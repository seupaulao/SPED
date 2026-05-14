## aplicacao lancamento contabil

Quero criar uma aplicação em python desktop offline, usando conceitos 
similares ao aplicativo `hledger` e uma base local em `contabilidade.db`
preparada para partidas dobradas e crédito e débito.

O intuito é fazer a contabilidade de diversas empresas ou entidades
que tenham contrato com minha empresa de contabilidade.

### status atual da implementacao

No estado atual do projeto, os itens abaixo ja estao implementados em `pjlacontabilidade.py`:

- menu principal em modo terminal
- selecao de empresa por codigo, nome ou cnpj
- cadastro, alteracao, listagem paginada e exclusao de empresa
- criacao de lancamento no livro diario com validacao de partidas dobradas
- correcao de lancamento existente
- exclusao de lancamento existente
- visualizacao resumida de lancamentos
- relatorios de balancete, balanco patrimonial, DRE e DVA em formato texto

Os itens abaixo continuam pendentes de detalhamento funcional:

- geracao do ECD/SPED

### banco de dados

o banco é em sqlite3 e está disponivel no arquivo `contabilidade.db`
foi criado a partir do script de criação em `banco_sqlite3.sql`

#### observacoes do schema atual

Para suportar os relatorios e a aplicacao atual, a tabela `plano_contas`
considera tambem os campos abaixo:

- `grupo`
- `dre_grupo`
- `subgrupo`
- `fluxo_caixa_tipo`

Tambem sao usados indices para melhorar consultas por data e conta:

- `idx_lancamento_data`
- `idx_lancamento_item_conta`

#### padrão de nomenclatura das contas (estilo hledger)

As contas devem ser nomeadas seguindo o padrão do aplicativo `hledger`, onde o nome
é composto por categorias separadas por `:` (dois-pontos). Isso facilita a hierarquização
e a legibilidade, além de permitir futura integração com hledger ou conversão de dados.

**Estrutura recomendada:**

```
[tipo]:[categoria]:[subcategoria]:[detalhe]
```

**Tipos permitidos (primeira parte do nome):**

- `ativo` — contas de ativo (bens e direitos)
- `passivo` — contas de passivo (obrigações)
- `receita` — contas de receita/entrada
- `despesa` — contas de despesa/saída
- `patrimonioliquido` — contas de patrimônio líquido

**Exemplos válidos:**

- `ativo:bank:conta_corrente` — conta bancária no ativo
- `ativo:caixa` — caixa (sem subcategorias)
- `passivo:fornecedores` — fornecedores a pagar
- `passivo:duplicatas_a_pagar` — duplicatas vencidas
- `receita:vendas:produto` — receita de venda de produto
- `receita:servicos:medicos` — receita de serviços médicos
- `despesa:inss` — despesa com INSS
- `despesa:salarios:clt` — despesa com salários de CLT
- `patrimonioliquido:lucros` — lucros acumulados

**Regras de nomenclatura:**

1. Comece sempre com um dos tipos acima
2. Use `:` (dois-pontos) como separador entre níveis
3. Use `_` (underscore) para separar palavras dentro de um nível
4. Use apenas minúsculas
5. Evite espaços e caracteres especiais

**Mapeamento interno:**

A aplicação mapeia automaticamente esses nomes para a estrutura de `plano_contas`:

- O **tipo** (primeira parte) define o `grupo` (ATIVO, PASSIVO, PL) ou classificação
- As **subcategorias** são armazenadas na coluna `descricao` exatamente como digitadas
- O **nível** da hierarquia é determinado automaticamente pela profundidade
- A **natureza** (D ou C) é inferida pelo tipo (ativo/despesa = D, passivo/receita = C)

Isso permite que o operador entre os nomes de forma amigável e o sistema cuide
da organização contábil interna.

### desenvolvimento

O desenvolvimento será por etapas:

1. registro do lançamento no livro diario

2. calculo do saldo de cada conta por periodo

3. elaboração do balanço patrimonial da entidade

4. elaboração do balancete da entidade

5. elaboração do DRE da entidade

6. elaboração do DVA da entidade

7. geração do SPED para enviar o ECD

### arquivo da aplicação

o nome do arquivo da aplicação será `pjlacontabilidade.py`

### menu da aplicação

ao entrar com a aplicação no terminal: `python pjlacontabilidade.py`
será aberta a aplicação, onde deve ser mostrado no
titulo do nome da aplicação `PJLA Contabilidade OFFLINE`
seguido por um menu que o usuário deve teclar a
letra correspondente da ação que ele deseja fazer.

```
[a] Livro Diario
[b] Relatórios
[c] Cadastro Empresa
[d] Gerar ECD
[q] Sair
```

O Livro Diário é a entrada principal do sistema e funciona conforme
regras na próxima seção.

As regras das demais funções serão feitas posteriomente nesse documento. 
E só devem ser implementadas quando forém registradas

### Inicio

Essa seção fica disponível apenas quando o usuário 
selecionar as opções do menu principal

- Livro Diário
- Relatórios
- Gerar ECD

**Funcionamento**

O sistema checa se existe empresas cadastradas, se não existir então:

```
Não há empresas cadastradas. Cadastre uma Empresa no Menu Principal. Clique para voltar ao Menu Principal.
```

Caso haja empresas cadastradas então:

A primeira pergunta para cada opção do menu principal
que será apresentada ao usuário será:

`Qual a empresa?`

entrada: o usuário digitará o código da empresa, o nome da empresa, ou seu cnpj.

Antes de imprimir o submenu, deve ser impresso : 

```
 EMPRESA: CODIGO_DA_EMPRESA - NOME_DA_EMPRESA
 CNPJ_DA_EMPRESA
```

Se não houver empresas cadastradas com os dados informados, deve ser apresentado:

```
Não encontrei nenhuma empresa cadastrada com os dados digitados. Clique para voltar ao Menu Principal."
```


### Menu Principal - Opção: Livro Diário 

**Submenu**

```
[a] Criar Lançamento
[b] Corrigir Lançamento
[c] Apagar Lançamento
[d] Visualizar todos os Lançamentos
[e] Voltar ao menu principal
```

**entrada de dados para lançamento de dados**

a entrada de dados vai obedecer o padrão hledger,
porém a diferença é:

Vai ser gravado o débito e o crédito correspondente de cada conta.
O crédito não será um lançamento negativo representado como no hledger.

Vai ser usado para entrada a seguinte forma:

```
### Entrada para DEBITO em uma CONTA

Iniciar os lançamentos

qual a conta? `NOME_DA_CONTA`
valor: `VALOR_ENTRADA` 

### Entrada para CREDITO em uma CONTA

qual a conta? `a NOME_DA_CONTA`
valor: `VALOR_ENTRADA`
```

A diferenciação de crédito ou débito não será pelo valor ser 
positivo ou negativo, será por colocar a partícula `a` na frente
do nome da conta. 
Ao colocar a partícula `a` necessariamente será feito um CREDITO
na conta.
Ao não colocar a particula `a`, será feito um DEBITO na conta.

Ao digitar '.' no campo 'qual a conta' ou 'VALOR'
ou teclar ENTER no campo VALOR vazio,
automaticamente o sistema encerrará os lançamentos
e validará se houve entradas válidas conforme a regra abaixo:

`Se no lançamento a soma dos DEBITOS é igual a soma dos CREDITOS`

Se o lançamento efetuado foi válido o sistema perguntará 
se deseja salvar, caso positivo deverá ser salvo na base de dados.
Se o lançamento for válido, e gravado com sucesso
automaticamente o sistema continua e pede um novo lançamento
Caso contrário, se o lançamento for inválido, ou se o lançamento
foi vazio o sistema entende que o usuário deseja voltar
para o menu da seção.

**Submenu Corrigir Lancamento**

Na correcao de lancamento, o sistema deve:

1. mostrar os ultimos lancamentos da empresa selecionada
2. solicitar o `ID` do lancamento que sera corrigido
3. exibir os dados atuais do lancamento e seus itens
4. permitir alterar `data`, `historico` e `numero`, usando `ENTER` para manter o valor atual
5. solicitar novamente todas as partidas do lancamento
6. validar novamente se a soma dos debitos e igual a soma dos creditos
7. pedir confirmacao para salvar a correcao

Na implementacao atual, a correcao substitui integralmente os itens do lancamento.

**Submenu Apagar Lancamento**

Na exclusao de lancamento, o sistema deve:

1. mostrar os ultimos lancamentos da empresa selecionada
2. solicitar o `ID` do lancamento que sera apagado
3. exibir os dados do lancamento e seus itens
4. pedir confirmacao antes de apagar
5. apagar o cabecalho e os itens correspondentes em transacao unica

**Submenu Visualizar todos os Lancamentos**

Na implementacao atual, a visualizacao lista os lancamentos mais recentes
da empresa selecionada, mostrando:

Usar a consulta
```sql
select lan.id, lan.numero, conta.codigo, lan.data, conta.descricao, item.tipo, item.valor 
from lancamento as lan inner join lancamento_item item on lan.id = item.lancamento_id,
                   plano_contas as conta on conta.id = item.conta_id
where empresa_id = ID_DA_EMPRESA
```

- `ID`
- `NUMERO`
- `CODIGO`
- `DATA`
- `DESCRICAO`
- `TIPO`
- `VALOR`

Hoje a tela mostra os 10 lancamentos mais recentes e retorna ao submenu apos confirmacao do usuario.

### Menu Principal - Opção : Relatórios

**Submenu**

```
[b] Balancete
[c] Balanço Patrimonial
[d] DRE
[e] DVA
[f] Voltar
```

Para qualquer um dos relatórios, deve ser solicitado o período:

```
Indique o Período:
De: DATA_INICIAL [Formato DD/MM/AAAA] [ENTER]
Até:  DATA_FINAL [Formato DD/MM/AAAA] [ENTER]
```

O sistema deve calcular o relatório correspondente e exibir na tela/console no formato texto 

Para o código dos relatórios o sistema pode usar como base o arquivo `funcoes_relatorios.py`

Na implementacao atual, os relatorios ja filtram os dados pela empresa selecionada.

Caso o usuário tecle a última opção, o sistema volta a tela anterior, no caso o Menu Principal.


### Menu Principal - Opção : Cadastro Empresa

**Submenu**

```
[a] Cadastrar
[b] Alterar
[c] Listar
[d] Excluir
[f] Voltar
```


**Submenu Cadastrar**
A lista composta dos campos da tabela empresas em 'contabilidade.db' deve ser exibido um a um
tratado o valor exibindo mensagem de erro caso o valor digitado não corresponda ao tipo de dado
informado.

Ao final uma mensagem: `Deseja salvar a informação? (s/n)` 
Deve aparecer ao preencher todos os dados da empresa/entidade

Se salvo corretamente volta ao submenu; caso haja erro ao salvar, exibe a mensagem de erro e ao usuário clicar em qualquer tecla volta ao submenu.
Caso o usuário tecle 'n' na pergunta anterior, volta para o submenu.

**Submenu Listar**
Uma consulta paginada de 10 itens será exibida na tela contendo as informações básicas da empresa

CODIGO NOME CNPJ

**Submenu Alterar**

Deve ser solicitado o CODIGO do registro que deve ser alterado

```
Qual o CODIGO da EMPRESA que deseja ALTERAR? Digite '.' para voltar ao submenu.
```

Em seguida o formulario com os dados padrão são carregados um a um para o usuário confirmar o valor ou 
digitar um novo valor, conforme o exemplo:

```
Digite o novo NOME da empresa, ou tecle ENTER para CONFIRMAR o valor atual
NOME (EMPRESA XYZ): 

Digite o novo CNPJ da empresa, ou tecle ENTER para CONFIRMAR o valor atual
CNPJ (111.111.111/0001-11): 
```

observar os campos do 'banco de dados'

**Submenu Excluir**
```
Deseja excluir essa entidade e TODOS seus dados? (s/n)
```

Caso seja digitado 's', apaga a empresa e todos os seus dados do banco
Caso contrário, volta ao submenu.

**Submenu Voltar**

Ao selecionar a letra correspondente, volta ao menu principal.

### próximos passos

Com base no estado atual da implementacao, os proximos passos recomendados sao:

1. detalhar e implementar edicao pontual de itens do lancamento, sem exigir redigitacao completa de todas as partidas
2. detalhar a geracao do ECD/SPED para substituir o placeholder atual da opcao `Gerar ECD`
3. criar um fluxo de carga inicial de plano de contas por empresa, para permitir uso real do Livro Diario sem depender de cadastro manual direto no banco





