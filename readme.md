# PJLA Contabilidade OFFLINE

Aplicação de contabilidade offline com suporte completo a Livro Diário, Relatórios e Plano de Contas, desenvolvida em Python com banco de dados SQLite.

## 📋 Versões

### `pjlacontabilidade.py` (Original)
Versão original com interface de linha de comando (CLI) usando inputs e prints.

**Recursos:**
- ✅ Cadastro de empresas (criar, alterar, listar, excluir)
- ✅ Livro Diário (criar, corrigir, apagar, visualizar lançamentos)
- ✅ Plano de Contas (nova conta, editar, listar, detalhar)
- ✅ Relatórios (Balancete, Balanço Patrimonial, DRE, DVA)
- ✅ ECD (em desenvolvimento)
- ✅ Validação de datas, valores decimais e moeda
- ✅ Banco de dados SQLite com PRAGMA foreign_keys

---

### `experiencia02.py` (Moderna com Textual)
Versão refatorada com interface moderna usando a biblioteca **Textual**, oferecendo uma experiência de usuário profissional com navegação intuitiva e formulários aprimorados.

## 🎨 Melhorias Implementadas na Versão Textual

### **1. Interface Moderna**
- Menu principal com botões visuais e atalhos de teclado
- Telas organizadas com Header e Footer
- Notificações toast para feedback do usuário
- Design responsivo e elegante

### **2. Componentes Reutilizáveis**
- **`FormField`** - Campo de entrada com label e validação
- **`EmpresaForm`** - Formulário completo para dados de empresa
- **`ContaForm`** - Formulário dinâmico para cadastro de contas
- **`MessageBox`** - Caixa de mensagem reutilizável

### **3. Screens (Telas) Implementadas**
- **`MainScreen`** - Menu principal interativo
- **`EmpresaListScreen`** - Listagem de empresas com DataTable
- **`EmpresaFormScreen`** - Cadastro/edição de empresa com validação
- **`ContaListScreen`** - Listagem de contas com ações inline
- **`ContaFormScreen`** - Cadastro/edição de contas com validação

### **4. Navegação Melhorada**
- Stack de telas com `push_screen()` e `pop_screen()`
- Atalhos de teclado intuitivos (Ctrl+S para salvar, ESC para voltar)
- Transições suaves entre telas
- Validação de formulários antes da submissão

### **5. DataTable para Listagem**
- Visualização profissional de dados
- Navegação com setas do teclado
- Integração com ações (editar, nova entrada)

## ⌨️ Atalhos de Teclado

### Menu Principal
| Tecla | Ação |
|-------|------|
| **A** | Livro Diário |
| **B** | Relatórios |
| **C** | Cadastro de Empresa |
| **E** | Plano de Contas |
| **Q** | Sair |

### Em Formulários
| Tecla | Ação |
|-------|------|
| **Ctrl+S** | Salvar |
| **ESC** | Cancelar |

### Em Listagens
| Tecla | Ação |
|-------|------|
| **N** | Nova entrada |
| **E** | Editar selecionado |
| **ESC** | Voltar |

## 🗄️ Estrutura do Banco de Dados

### Tabelas Principais
- **`empresa`** - Cadastro de empresas
- **`plano_contas`** - Plano de contas com suporte a conta analítica/sintética
- **`lancamento`** - Cabeçalho de lançamentos (escrituração)
- **`lancamento_item`** - Itens de lançamento (débito/crédito)
- **`mapa_demonstracoes`** - Mapeamento para demonstrações

### Campos de Empresa
| Campo | Tipo | Obrigatório |
|-------|------|------------|
| `cnpj` | TEXT | Sim |
| `nome` | TEXT | Sim |
| `uf` | TEXT | Não |
| `municipio` | TEXT | Não |
| `data_inicio` | DATE | Não |
| `data_fim` | DATE | Não |

### Campos de Plano de Contas
| Campo | Tipo | Descrição |
|-------|------|-----------|
| `empresa_id` | FK | Referência à empresa |
| `codigo` | TEXT | Ex: 01.01.01 |
| `descricao` | TEXT | Nome da conta |
| `tipo` | TEXT | A (Analítica) ou S (Sintética) |
| `natureza` | TEXT | D (Devedora) ou C (Credora) |
| `grupo` | TEXT | Agrupamento |
| `dre_grupo` | TEXT | Classificação DRE |
| `subgrupo` | TEXT | Subagrupamento |
| `fluxo_caixa_tipo` | TEXT | Tipo de fluxo de caixa |

## 🚀 Como Usar

### Requisitos
```bash
pip install textual
```

### Executar a Aplicação
```bash
python experiencia02.py
```

### Usar a Versão CLI Original
```bash
python pjlacontabilidade.py
```

## 📁 Estrutura de Arquivos

```
├── pjlacontabilidade.py          # Versão original (CLI)
├── experiencia02.py              # Versão moderna (Textual)
├── banco_sqlite3.sql             # Schema do banco de dados
├── contabilidade.db              # Base de dados (gerada automaticamente)
├── funcoes_relatorios.py         # Funções de relatórios
└── README.md                     # Este arquivo
```

## 🔧 Funcionalidades Principais

### Cadastro de Empresa
- ✅ Criar nova empresa
- ✅ Alterar dados da empresa
- ✅ Listar empresas (paginação na versão CLI)
- ✅ Excluir empresa e todos seus dados

### Livro Diário
- ✅ Criar lançamentos (escrituração)
- ✅ Validação de débito = crédito
- ✅ Corrigir lançamentos existentes
- ✅ Apagar lançamentos
- ✅ Visualizar últimos lançamentos
- 🔜 Lançamentos de estorno
- 🔜 Lançamentos de ajuste

### Plano de Contas
- ✅ Criar nova conta
- ✅ Editar conta existente
- ✅ Detalhar conta (mostrar todos os campos)
- ✅ Listar todas as contas
- 🔜 Excluir conta com validação

### Relatórios
- ✅ Balancete (período)
- ✅ Balanço Patrimonial
- ✅ DRE (Demonstração de Resultado do Exercício)
- ✅ DVA (Demonstração de Valor Adicionado)

## 🎯 Validações Implementadas

### Datas
- Formato: DD/MM/AAAA ou YYYY-MM-DD
- Normalização automática para YYYY-MM-DD

### Valores Monetários
- Suporte a separadores: . (ponto) e , (vírgula)
- Valores devem ser maiores que zero
- Formatação em BRL com duas casas decimais

### Campos Obrigatórios
- Validação em tempo de entrada
- Mensagens de erro descritivas
- Rollback de transações em caso de erro

## 🔐 Segurança

- ✅ Transações ACID com BEGIN/COMMIT/ROLLBACK
- ✅ Foreign keys habilitadas (PRAGMA)
- ✅ Índices para melhor performance
- ✅ Validação de entrada em todos os campos

## 🐛 Tratamento de Erros

Todos os erros de banco de dados são tratados com:
- Rollback automático
- Mensagens de erro amigáveis
- Opção de repetir a operação

## 📊 Exemplo de Uso

### Criar uma Empresa
```
1. Pressionar [C] no menu principal
2. Clicar em "Salvar"
3. Preencher formulário com:
   - CNPJ: 12.345.678/0001-90
   - Nome: Empresa Exemplo LTDA
4. Pressionar Ctrl+S
```

### Registrar Lançamento
```
1. Pressionar [A] para Livro Diário
2. Selecionar empresa
3. Preencher data, histórico e número do documento
4. Adicionar contas com D (débito) ou A (crédito)
5. Validação automática: débito = crédito
```

## 🔄 Roadmap Futuro

- [ ] Relatório completo em PDF
- [ ] Exportação em Excel
- [ ] Integração com ECD (Escrituração Contábil Digital)
- [ ] Suporte a múltiplos períodos
- [ ] Dashboard com resumo financeiro
- [ ] Autenticação de usuários
- [ ] Sincronização com nuvem

## 📝 Licença

Este projeto é de código aberto e pode ser utilizado livremente.

## 👤 Autor

**seupaulao** - SPED Project

---

**Versão Atual:** 2.0 (Textual UI)  
**Data de Atualização:** 2026-05-17  
**Status:** Ativo - Em desenvolvimento
