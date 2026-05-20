# PJLA Contabilidade OFFLINE

Aplicação de contabilidade offline em Python + SQLite, com interface TUI baseada em Textual e versão CLI legada.

## Visão Geral

O projeto possui duas interfaces principais:

1. [pjlacontabilidade.py](pjlacontabilidade.py): versão CLI original.
2. [experiencia02.py](experiencia02.py): versão Textual modularizada.

## Arquitetura Atual da Versão Textual

O arquivo [experiencia02.py](experiencia02.py) foi simplificado e agora concentra:

1. `MainScreen` (menu principal).
2. Importação das telas.
3. Ponto de entrada da aplicação (`run_app(MainScreen)`).

As demais telas foram separadas por domínio no padrão `experiencia02_tela_NOME_TELA.py`.

## Estrutura de Arquivos (Textual)

- [experiencia02.py](experiencia02.py): tela principal e entrada.
- [experiencia02_tela_app.py](experiencia02_tela_app.py): bootstrap do app Textual e CSS global.
- [experiencia02_tela_estado.py](experiencia02_tela_estado.py): estado compartilhado (empresa atual).
- [experiencia02_tela_componentes.py](experiencia02_tela_componentes.py): componentes reutilizáveis (`FormField`, `ConfirmDialog`, etc.).
- [experiencia02_tela_empresa.py](experiencia02_tela_empresa.py): CRUD de Empresa.
- [experiencia02_tela_contas.py](experiencia02_tela_contas.py): CRUD de Plano de Contas.
- [experiencia02_tela_livro_diario.py](experiencia02_tela_livro_diario.py): Livro Diário e edição de lançamentos.
- [experiencia02_tela_relatorios.py](experiencia02_tela_relatorios.py): tela de relatórios.
- [experiencia02_tela_set_empresa.py](experiencia02_tela_set_empresa.py): seleção de empresa atual.
- [experiencia02_tela_plano_referencial.py](experiencia02_tela_plano_referencial.py): CRUD de Plano de Contas Referencial.
- [experiencia02_tela_usuarios.py](experiencia02_tela_usuarios.py): CRUD de Usuários.
- [experiencia02_tela_centro_custos.py](experiencia02_tela_centro_custos.py): CRUD de Centro de Custos.
- [experiencia02_tela_tags.py](experiencia02_tela_tags.py): CRUD de Tags.
- [experiencia02_tela_certificados_digitais.py](experiencia02_tela_certificados_digitais.py): CRUD de Certificados Digitais.
- [experiencia02_tela_assinaturas_digitais.py](experiencia02_tela_assinaturas_digitais.py): CRUD de Assinaturas Digitais.

## Funcionalidades Implementadas

### Núcleo contábil

- Cadastro e edição de empresas.
- Definição da empresa ativa para o contexto de trabalho.
- Cadastro e edição de plano de contas por empresa.
- Livro diário com inclusão, edição e exclusão de lançamentos e itens.

### Cadastros auxiliares

- Plano de contas referencial.
- Usuários.
- Centro de custos.
- Tags.
- Certificados digitais.
- Assinaturas digitais.

## Atalhos de Teclado

### Menu principal

| Tecla | Ação |
|-------|------|
| A | Livro Diário |
| B | Relatórios |
| C | Empresa |
| D | Definir Empresa |
| E | Contas |
| F | Plano Referencial |
| G | Usuários |
| H | Centro de Custos |
| I | Tags |
| J | Certificados Digitais |
| K | Assinaturas Digitais |
| Q | Sair |

### Listagens e formulários

| Tecla | Ação |
|-------|------|
| N | Novo registro (listagens) |
| E | Editar registro selecionado (listagens) |
| D | Excluir registro selecionado (listagens) |
| Ctrl+S | Salvar (formulários) |
| Esc | Voltar/Cancelar |

## Banco de Dados

Schemas principais:

1. [banco_sqlite3.sql](banco_sqlite3.sql)
2. [banco_sqlite3_novo.sql](banco_sqlite3_novo.sql)

Tabelas relevantes para a versão Textual:

- `empresa`
- `plano_contas`
- `lancamento`
- `lancamento_item`
- `plano_contas_referencial`
- `usuarios`
- `centro_custo`
- `tags`
- `certificados_digitais`
- `assinaturas_digitais`

## Execução

### Requisitos

Instale as dependências do projeto (preferencialmente em ambiente virtual):

```bash
pip install -r requirements.txt
```

### Executar versão Textual

```bash
python experiencia02.py
```

### Executar versão CLI legada

```bash
python pjlacontabilidade.py
```

## Validação e Qualidade

Para validar sintaxe da versão modular:

```bash
python -m py_compile experiencia02.py experiencia02_tela_*.py
```

## Situação Atual e Próximos Passos

### Concluído recentemente

- Modularização da versão Textual por tela.
- Padronização de telas CRUD com DataTable + formulário + confirmação de exclusão.
- Inclusão dos novos módulos de cadastro auxiliar no menu principal.

### Itens em evolução

- Evoluir a tela de relatórios para além do placeholder.
- Melhorar UX de busca/seleção de contas no lançamento.
  - não permite entrar com contas, não está reconhecendo a empresa pre-selecionada
  - ao lado do campo conta deve haver um botão que abre uma modal com o datatable
  e nele o plano de contas da empresa pre-selecionada. Quando o usuario clicar na
  conta, ela deve voltar o codigo para o campo da tela de lancamento_item
  - Fazer 2 modos de entrada do diario:

  1. Igual a `pjlacontabilidade.py`, ou seja identificando o debito e o credito através da 
  descricao do campo no formato das formulas de escrituracao:
```
  conta             VALOR
  a conta           VALOR
```
  A particula 'a' na frente da conta indica que o lancamento é a crédito, caso contrário
  o lançamento é a debito.

  Para validar o lançamento: a soma dos lancamentos_item de crédito deve ser igual a soma dos 
  lançamentos_item a debito

  2. De acordo com a tela já existente em `experiencia02_tela_livro_diario.py` 
- Revisar consistência entre nomes de tabelas/FKs no schema novo para módulos avançados.
- Definir controle de acesso por perfil de usuário.

- No MainScreen colocar o componente Select e criar as opções conforme
as telas relacionadas da aplicação:
  - Definir Empresa
  - Empresa
  - Livro Diário
  - Assinaturas Digitais
  - Certificados Digitais
  - Centro de Custos
  - Plano Contas Referencial
  - Plano Contas
  - Relatorios
  - Usuarios
  - Tags
  - Sair

- Em Footer deixar apenas as seguintes opções:
  - Sair
  - Definir Empresa
  - Empresa
  - Livro Diário
  


## 📝 Licença

Este projeto é de código aberto e pode ser utilizado livremente.

## 👤 Autor

**seupaulao** - SPED Project

---

**Versão Atual:** 2.1 (Textual UI modular)  
**Data de Atualização:** 2026-05-20  
**Status:** Ativo - Em desenvolvimento

