# Análise das Tabelas do Banco de Dados - PJLA Contabilidade

Documentação completa das tabelas do banco `contabilidade.db`, projetado para uma aplicação de escritório contábil com suporte a múltiplas empresas, partidas dobradas e geração automática de relatórios.

---

## Tabela: `empresa`

Armazena os dados cadastrais das entidades (clientes) para as quais o escritório contábil presta serviços.

### Campos

- **`id`** (INTEGER PRIMARY KEY AUTOINCREMENT)  
  Identificador único da empresa. Chave primária gerada automaticamente.

- **`cnpj`** (TEXT NOT NULL)  
  Número CNPJ da empresa. Campo obrigatório, identifica a empresa legalmente. Deve ser armazenado como texto para preservar zeros à esquerda e formatação.

- **`nome`** (TEXT NOT NULL)  
  Razão social ou nome da empresa. Campo obrigatório para identificação visual.

- **`uf`** (TEXT)  
  Unidade da Federação (estado) onde a empresa está localizada (ex: `SP`, `RJ`, `MG`). Opcional, usado para endereço fiscal.

- **`municipio`** (TEXT)  
  Município onde a empresa está localizada. Opcional, complementa a localização fiscal.

- **`data_inicio`** (TEXT)  
  Data de início das atividades ou da vigência do contrato com o escritório (formato: `YYYY-MM-DD`). Opcional, define o período contábil inicial.

- **`data_fim`** (TEXT)  
  Data de encerramento das atividades ou término do contrato (formato: `YYYY-MM-DD`). Opcional, permite marcar empresas inativas.

- **`created_at`** (TEXT DEFAULT CURRENT_TIMESTAMP)  
  Data/hora de criação do registro no banco, para auditoria.

### Relacionamentos

- **1:N com `plano_contas`**: cada empresa tem seu próprio plano de contas
- **1:N com `lancamento`**: cada empresa tem múltiplos lançamentos contábeis
- **1:N com `historico_padrao`**: cada empresa pode ter descrições padrão de lançamentos

### Importância

Tabela fundamental que permite o isolamento de dados entre clientes. Cada operação subsequente (plano de contas, lançamentos, relatórios) é filtrada por `empresa_id` para evitar mistura de dados.

---

## Tabela: `plano_contas`

Armazena a hierarquia de contas contábeis de cada empresa. É o núcleo do sistema, pois todo lançamento referencia contas dessa tabela.

### Campos

#### Identificação

- **`id`** (INTEGER PRIMARY KEY AUTOINCREMENT)  
  Identificador único da conta. Gerado automaticamente para cada novo registro.

- **`empresa_id`** (INTEGER, FOREIGN KEY)  
  Referência à empresa proprietária da conta. Permite que múltiplas empresas tenham seus próprios planos de contas isolados.

- **`codigo`** (TEXT NOT NULL)  
  Código/número da conta na hierarquia contábil (ex: `1.1.1.01`, `2.2.1`). Segue a estrutura do plano de contas brasileiro. É único por empresa.

- **`descricao`** (TEXT NOT NULL)  
  Nome/descrição legível da conta (ex: `Caixa`, `Fornecedores`, `Receita de Vendas`).

#### Classificação Contábil

- **`tipo`** (TEXT NOT NULL, valores: `S` ou `A`)  
  Define o nível da conta na hierarquia:
  - `S` = **Sintética**: contas agregadoras que agrupam outras contas. Nunca recebem lançamentos diretos.
  - `A` = **Analítica**: contas que recebem lançamentos efetivos.

- **`natureza`** (TEXT, valores: `D` ou `C`)  
  Define o saldo natural da conta:
  - `D` = **Devedora**: aumenta com débito, diminui com crédito (Ativo, Despesa)
  - `C` = **Credora**: aumenta com crédito, diminui com débito (Passivo, Receita)

#### Posicionamento Hierárquico

- **`nivel`** (INTEGER NOT NULL)  
  Profundidade da conta na árvore (ex: 1 = contas raiz, 2 = subgrupos, 3 = contas analíticas). Usado para indentação visual.

- **`conta_pai_id`** (INTEGER, FOREIGN KEY autoreferencial)  
  Aponta para a conta que é o "pai" (supergrupo) na hierarquia. Permite estrutura em árvore.

#### Classificação de Relatórios

- **`grupo`** (TEXT)  
  Classificação no Balanço Patrimonial:
  - `ATIVO`: bens e direitos
  - `PASSIVO`: obrigações
  - `PL`: patrimônio líquido

- **`dre_grupo`** (TEXT)  
  Classificação na Demonstração do Resultado (DRE):
  - `RECEITA_BRUTA`: receitas operacionais
  - `CUSTO`: custo dos produtos vendidos
  - `DESPESA_OPERACIONAL`: despesas gerais
  - `RESULTADO_FINANCEIRO`: juros e variações financeiras

- **`subgrupo`** (TEXT)  
  Classificação na Demonstração do Valor Adicionado (DVA):
  - `RECEITAS`, `INSUMOS`, `PESSOAL`, `IMPOSTOS`, `CAPITAL_TERCEIROS`

- **`fluxo_caixa_tipo`** (TEXT)  
  Classificação no Fluxo de Caixa (DFC):
  - `OPERACIONAL`: atividades operacionais
  - `INVESTIMENTO`: compra/venda de ativos
  - `FINANCIAMENTO`: empréstimos e dividendos

#### Configuração

- **`codigo_referencial`** (TEXT)  
  Código externo para integração (ex: código SPED, referência legal).

- **`aceita_lancamento`** (INTEGER DEFAULT 1)  
  Flag de bloqueio:
  - `1` = aceita lançamentos (conta analítica)
  - `0` = bloqueada (conta sintética ou inativa)

- **`created_at`** (TEXT DEFAULT CURRENT_TIMESTAMP)  
  Data/hora de criação para auditoria.

### Relacionamentos

- **N:1 com `empresa`**: cada conta pertence a uma empresa
- **1:N (auto-relacionamento) via `conta_pai_id`**: hierarquia de contas
- **1:N com `lancamento_item`**: cada conta pode ter múltiplos itens de lançamento
- **1:N com `mapa_demonstracoes`**: cada conta pode estar mapeada em múltiplos relatórios

### Importância

Implementa um plano de contas hierárquico que permite estruturar contas por grupos, gerar relatórios automaticamente e bloquear lançamentos em contas sintéticas.

---

## Tabela: `historico_padrao`

Armazena descrições/históricos reutilizáveis para lançamentos, reduzindo digitação repetitiva.

### Campos

- **`id`** (INTEGER PRIMARY KEY AUTOINCREMENT)  
  Identificador único do histórico padrão.

- **`empresa_id`** (INTEGER, FOREIGN KEY)  
  Referência à empresa. Cada empresa pode ter seus próprios históricos.

- **`codigo`** (TEXT)  
  Código de referência para o histórico (ex: `VND001` para "Venda a Cliente", `CHQ002` para "Cheque emitido").

- **`descricao`** (TEXT NOT NULL)  
  Texto do histórico a reutilizar (ex: `Venda de produtos - NF 001`, `Depósito bancário - Cheque 12345`).

### Relacionamentos

- **N:1 com `empresa`**: cada histórico pertence a uma empresa
- **1:N com `lancamento`**: um histórico padrão pode ser referenciado por múltiplos lançamentos

### Importância

Melhora a usabilidade da aplicação ao permitir que o operador selecione um histórico pré-configurado em vez de digitar manualmente. Essencial em operações repetitivas (folha de pagamento, depósitos, transferências).

---

## Tabela: `lancamento`

Armazena o **cabeçalho** de cada lançamento contábil. Um lançamento é composto por um cabeçalho + múltiplos itens de débito/crédito (partidas dobradas).

### Campos

- **`id`** (INTEGER PRIMARY KEY AUTOINCREMENT)  
  Identificador único do lançamento.

- **`empresa_id`** (INTEGER, FOREIGN KEY)  
  Referência à empresa. Isola lançamentos por cliente.

- **`data`** (TEXT NOT NULL)  
  Data do lançamento contábil (formato: `YYYY-MM-DD`). Define o período fiscal ao qual pertence.

- **`numero`** (TEXT)  
  Número de referência do documento (ex: número da nota fiscal, cheque, recibo). Opcional, usado para rastreabilidade.

- **`historico`** (TEXT)  
  Descrição do lançamento digitada pelo operador (ex: `Venda de produto para cliente XYZ`). Campo livre.

- **`historico_padrao_id`** (INTEGER, FOREIGN KEY)  
  Referência a um histórico pré-configurado. Permite vincular um modelo de descrição ao lançamento.

- **`valor_total`** (REAL)  
  Valor total do lançamento (soma dos débitos ou créditos, que devem ser iguais em partidas dobradas). Desnormalizado para aceleração de consultas.

- **`tipo`** (TEXT DEFAULT 'N')  
  Tipo de lançamento:
  - `N` = Normal (lançamento padrão)
  - Pode ser expandido para outros tipos (ex: `E` = Estorno, `A` = Ajuste)

- **`created_at`** (TEXT DEFAULT CURRENT_TIMESTAMP)  
  Data/hora de criação para auditoria.

### Relacionamentos

- **N:1 com `empresa`**: cada lançamento pertence a uma empresa
- **N:1 com `historico_padrao`**: pode referenciar um histórico pré-configurado
- **1:N com `lancamento_item`**: um lançamento tem múltiplos itens de débito/crédito

### Importância

Lançamento é a unidade central de entrada de dados. A regra fundamental de contabilidade (débito = crédito) é validada pelos itens associados.

---

## Tabela: `lancamento_item`

Armazena os **itens** (linhas) de cada lançamento, implementando a regra de **partidas dobradas**: cada transação tem débitos e créditos que se equilibram.

### Campos

- **`id`** (INTEGER PRIMARY KEY AUTOINCREMENT)  
  Identificador único do item.

- **`lancamento_id`** (INTEGER, FOREIGN KEY com ON DELETE CASCADE)  
  Referência ao lançamento pai. Se o lançamento for deletado, todos os itens são removidos automaticamente.

- **`conta_id`** (INTEGER, FOREIGN KEY)  
  Referência à conta contábil que receberá o débito ou crédito.

- **`tipo`** (TEXT NOT NULL, valores: `D` ou `C`)  
  Define se é débito ou crédito:
  - `D` = Débito (afeta a conta conforme sua natureza)
  - `C` = Crédito (afeta a conta conforme sua natureza)

- **`valor`** (REAL NOT NULL)  
  Valor do débito ou crédito, sempre positivo. A soma dos débitos deve igualar a soma dos créditos.

- **`historico`** (TEXT)  
  Histórico específico para este item (opcional, pode diferir do histórico geral do lançamento).

### Relacionamentos

- **N:1 com `lancamento`**: múltiplos itens pertencem a um lançamento
- **N:1 com `plano_contas`**: cada item afeta uma conta específica

### Importante: Regra de Partidas Dobradas

Para que um lançamento seja válido:
$$\sum \text{débitos} = \sum \text{créditos}$$

Exemplo de lançamento válido:
| Tipo | Conta | Valor |
|------|-------|-------|
| D | Caixa | 1.000 |
| C | Receita | 1.000 |

### Importância

Implementa o princípio contábil fundamental. A aplicação bloqueia lançamentos desbalanceados. Índice em `lancamento_id` e `conta_id` melhora performance de relatórios.

---

## Tabela: `mapa_demonstracoes`

Mapeia contas para demonstrações financeiras específicas, permitindo gerar relatórios como DRE, DVA e DFC mesmo que a conta não tenha campos específicos preenchidos.

### Campos

- **`id`** (INTEGER PRIMARY KEY AUTOINCREMENT)  
  Identificador único do mapeamento.

- **`conta_id`** (INTEGER, FOREIGN KEY)  
  Referência à conta contábil a ser mapeada.

- **`tipo`** (TEXT)  
  Tipo de demonstração para a qual a conta será mapeada:
  - `DRE` = Demonstração do Resultado (relatório de lucro/prejuízo)
  - `DVA` = Demonstração do Valor Adicionado
  - `DFC` = Demonstração de Fluxo de Caixa

- **`categoria`** (TEXT)  
  Categoria específica dentro do relatório (ex: para DRE, pode ser `RECEITA_BRUTA`, `DESPESA`; para DVA, pode ser `PESSOAL`, `IMPOSTOS`).

### Relacionamentos

- **N:1 com `plano_contas`**: múltiplos mapeamentos para uma conta

### Importância

Fornece flexibilidade adicional para configurar relatórios. Se um campo como `dre_grupo` não for preenchido na conta, o mapeamento serve como alternativa de classificação. Essencial para adaptar o sistema a diferentes estruturas de relatório.

---

## Resumo da Arquitetura

### Fluxo de Dados

```
Empresa
  ├─ Plano de Contas (hierarquizado)
  │   └─ Mapa de Demonstrações (para relatórios)
  │
  ├─ Históricos Padrão (descrições reutilizáveis)
  │
  └─ Lançamentos (entrada de dados)
      └─ Itens de Lançamento (partidas dobradas)
```

### Isolamento Multi-Empresa

Todas as tabelas críticas (`plano_contas`, `lancamento`, `historico_padrao`) referem-se a `empresa_id`, garantindo que dados de diferentes clientes nunca se misturem.

### Validações Implícitas no Schema

- **Chaves estrangeiras**: evitam referências órfãs
- **NOT NULL**: campos obrigatórios
- **ON DELETE CASCADE**: ao deletar lançamento, itens são removidos automaticamente
- **Autorrelacionamento** em `plano_contas`: permite árvore hierárquica

### Índices para Performance

- `idx_lancamento_data`: consultas rápidas por período
- `idx_lancamento_item_conta`: agregações por conta e saldo

---

## Casos de Uso Principais

1. **Cadastrar Empresa**: inserir em `empresa`
2. **Montar Plano de Contas**: inserir hierarquia em `plano_contas`
3. **Registrar Lançamento**: 
   - inserir cabeçalho em `lancamento`
   - inserir múltiplos itens em `lancamento_item` (validando débito = crédito)
4. **Gerar Balancete**: agregar itens por conta, respeitar natureza
5. **Gerar BP/DRE/DVA**: agregar itens por grupo/dre_grupo/subgrupo, usando `mapa_demonstracoes` como fallback
6. **Auditoria**: verificar `created_at` em todas as tabelas
