# PJLA Contabilidade

Aplicação de contabilidade em Python com interface TUI baseada em Textual, banco SQLite (modo offline) e suporte a PostgreSQL via Docker.

## Visão Geral

A versão ativa do projeto encontra-se na pasta `src/` com os módulos renomeados para o padrão `pjla_contabil_*.py`. A pasta `projeto_offline/` preserva o estado anterior da aplicação (base SQLite + nomenclatura `experiencia02`).

## Arquitetura Atual da Versão Textual

O arquivo [src/pjla_contabil.py](src/pjla_contabil.py) concentra:

1. `MainScreen` (menu principal).
2. Importação das telas.
3. Ponto de entrada da aplicação (`run_app(MainScreen)`).

As demais telas estão separadas por domínio no padrão `pjla_contabil_tela_NOME_TELA.py`.

## Estrutura de Pastas e Arquivos

```
SPED/
├── Dockerfile                          ← container PostgreSQL
├── README.md
├── requirements.txt
├── clean_cache.sh
│
├── src/                                ← versão ativa
│   ├── pjla_contabil.py                ← entrada principal (MainScreen)
│   ├── pjla_contabil_tela_app.py       ← bootstrap do app Textual e CSS global
│   ├── pjla_contabil_tela_estado.py    ← estado compartilhado (empresa atual)
│   ├── pjla_contabil_tela_componentes.py ← componentes reutilizáveis (FormField, ConfirmDialog…)
│   ├── pjla_contabil_tela_empresa.py   ← CRUD de Empresa
│   ├── pjla_contabil_tela_contas.py    ← CRUD de Plano de Contas
│   ├── pjla_contabil_tela_livro_diario.py ← Livro Diário e lançamentos
│   ├── pjla_contabil_tela_relatorios.py   ← tela de relatórios
│   ├── pjla_contabil_tela_set_empresa.py  ← seleção de empresa ativa
│   ├── pjla_contabil_tela_plano_referencial.py ← CRUD de Plano Referencial
│   ├── pjla_contabil_tela_usuarios.py  ← CRUD de Usuários
│   ├── pjla_contabil_tela_centro_custos.py ← CRUD de Centro de Custos
│   ├── pjla_contabil_tela_tags.py      ← CRUD de Tags
│   ├── pjla_contabil_tela_certificados_digitais.py ← CRUD de Certificados Digitais
│   ├── pjla_contabil_tela_assinaturas_digitais.py  ← CRUD de Assinaturas Digitais
│   ├── pjla_contabil_backup_refactor.py
│   ├── funcoes_relatorios.py
│   ├── finantial_ratios.py
│   └── contabilidade.db                ← banco SQLite ativo
│
├── projeto_offline/                    ← backup da versão SQLite original
│   ├── experiencia02.py
│   ├── experiencia02_tela_*.py
│   ├── pjlacontabilidade.py            ← versão CLI legada
│   ├── app.py
│   ├── database.py
│   ├── funcoes_relatorios.py
│   ├── finantial_ratios.py
│   ├── contabilidade.db
│   ├── empresas.db
│   └── testes-*.py
│
├── scripts_banco_dados/
│   ├── banco_postgresql.sql            ← schema PostgreSQL (gerado a partir do SQLite)
│   ├── banco_sqlite3_novo.sql          ← schema SQLite atual
│   ├── banco_sqlite3.sql
│   └── (outros scripts de migração)
│
├── hledger/                            ← plano de contas e registros hledger
├── gerando_sped/                       ← arquivos gerados para SPED
└── venv/                               ← ambiente virtual Python
```

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

### SQLite (modo offline)

Schema ativo: [scripts_banco_dados/banco_sqlite3_novo.sql](scripts_banco_dados/banco_sqlite3_novo.sql)

Tabelas principais:

- `empresa`
- `plano_contas`
- `lancamento` / `lancamento_item`
- `plano_contas_referencial`
- `usuarios`
- `centro_custo`
- `tags`
- `certificados_digitais`
- `assinaturas_digitais`

### PostgreSQL (Docker)

Schema: [scripts_banco_dados/banco_postgresql.sql](scripts_banco_dados/banco_postgresql.sql)

Diferenças em relação ao SQLite:
- `BIGSERIAL` / `UUID` como chaves primárias
- `TIMESTAMP WITH TIME ZONE` nos campos de data
- `BOOLEAN` substituindo inteiros 0/1
- `BYTEA` substituindo `BLOB`
- `JSONB` nos campos de auditoria e payload de jobs

## Execução

### Requisitos

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Executar versão Textual (src/)

```bash
venv/bin/python src/pjla_contabil.py
```

### Validar sintaxe

```bash
venv/bin/python -m py_compile src/pjla_contabil.py src/pjla_contabil_tela_*.py
```

## Executando com PostgreSQL via Docker

### Pré-requisitos

```bash
# Ubuntu/Debian
sudo apt install docker.io -y
sudo systemctl start docker
sudo usermod -aG docker $USER   # requer logout/login para surtir efeito
```

### Build da imagem

```bash
docker build -t contabilidade-pg .
```

### Rodar o container

```bash
docker run -d \
  --name contabilidade-db \
  -p 5432:5432 \
  contabilidade-pg
```

- `-d` — roda em background
- `-p 5432:5432` — mapeia a porta para a máquina local

### Verificar logs

```bash
docker logs contabilidade-db
```

### Conectar via psql

```bash
docker exec -it contabilidade-db psql -U postgres -d contabilidade
```

## Situação Atual e Próximos Passos

### Concluído recentemente

- Modularização da versão Textual por tela.
- Padronização de telas CRUD com DataTable + formulário + confirmação de exclusão.
- Inclusão dos novos módulos de cadastro auxiliar no menu principal.
- Renomeação dos módulos de `experiencia02_*` para `pjla_contabil_*` em src.
- Geração do schema PostgreSQL (`banco_postgresql.sql`) a partir do SQLite.
- Criação do Dockerfile com PostgreSQL 16 e carga automática do schema.

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

  2. De acordo com a tela já existente em `pjla_contabil_tela_livro_diario.py`
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

**Versão Atual:** 3.0 (pjla_contabil + Docker)  
**Data de Atualização:** 2026-05-22  
**Status:** Ativo - Em desenvolvimento


---

Para aplicar, habilite as ferramentas de edição no VS Code e eu faço a substituição automaticamente, ou copie o conteúdo acima diretamente no arquivo [README.md](README.md).---

Para aplicar, habilite as ferramentas de edição no VS Code e eu faço a substituição automaticamente, ou copie o conteúdo acima diretamente no arquivo [README.md](README.md).

Completed: *Update README.md with new structure and Docker instructions* (8/8)