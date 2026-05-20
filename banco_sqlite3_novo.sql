PRAGMA foreign_keys = ON;

-- Converted from PostgreSQL to SQLite3

CREATE TABLE empresa (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  cnpj TEXT NOT NULL,
  nome TEXT NOT NULL,
  uf TEXT,
  municipio TEXT,
  data_inicio TEXT,
  data_fim TEXT,
  created_at TEXT DEFAULT (datetime('now')),
  excluido_at TEXT
);

-- =========================================================
-- TIPOS DE DEMONSTRAÇÕES
-- =========================================================

CREATE TABLE report_types (
    id TEXT PRIMARY KEY,
    code TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL
);

INSERT INTO report_types (id, code, name)
VALUES
(lower(hex(randomblob(16))), 'BALANCO', 'Balanço Patrimonial'),
(lower(hex(randomblob(16))), 'DRE', 'Demonstração do Resultado'),
(lower(hex(randomblob(16))), 'DFC', 'Demonstração do Fluxo de Caixa'),
(lower(hex(randomblob(16))), 'DVA', 'Demonstração do Valor Adicionado'),
(lower(hex(randomblob(16))), 'BALANCETE', 'Balancete');

CREATE TABLE plano_contas_referencial (
    id INTEGER PRIMARY KEY,
    codigo TEXT NOT NULL,
    nome TEXT NOT NULL,
    tipo TEXT,
    natureza TEXT,
    nivel INTEGER,
    parent_id INTEGER REFERENCES plano_contas_referencial(id),
    grupo TEXT,
    dre_grupo TEXT,
    fluxo_caixa_tipo TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    excluded_at TEXT
);

--(id, empresa_id, codigo, descricao, tipo, natureza, nivel, conta_pai_id, codigo_referencial, aceita_lancamento, created_at, grupo, subgrupo, dre_grupo, fluxo_caixa_tipo, excluido_at)

CREATE TABLE plano_contas (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  empresa_id INTEGER REFERENCES empresa(id),
  plano_contas_referencial_id INTEGER REFERENCES plano_contas_referencial(id),
  codigo TEXT NOT NULL,
  descricao TEXT NOT NULL,
  tipo TEXT NOT NULL,
  natureza TEXT,
  nivel INTEGER NOT NULL,
  conta_pai_id INTEGER REFERENCES plano_contas(id),
  codigo_referencial TEXT,
  aceita_lancamento INTEGER DEFAULT 1,
  grupo TEXT,
  subgrupo TEXT,
  dre_grupo TEXT,
  fluxo_caixa_tipo TEXT,
  created_at TEXT DEFAULT (datetime('now')),
  excluido_at TEXT
);

-- =========================================================
-- CENTRO DE CUSTO
-- =========================================================

CREATE TABLE centro_custo (
    id TEXT PRIMARY KEY,
    empresa_id TEXT NOT NULL REFERENCES empresa(id),
    codigo TEXT,
    nome TEXT NOT NULL,
    created_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE lancamento (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  empresa_id INTEGER REFERENCES empresa(id),
  data TEXT NOT NULL,
  historico TEXT,
  tipo TEXT DEFAULT 'N',
  created_at TEXT DEFAULT (datetime('now')),
  excluido_at TEXT
);

CREATE TABLE lancamento_item (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  lancamento_id INTEGER REFERENCES lancamento(id) ON DELETE CASCADE,
  conta_id INTEGER REFERENCES plano_contas(id),
  centro_custo_id TEXT REFERENCES centro_custo(id),
  tipo TEXT NOT NULL,
  valor NUMERIC(14,2) NOT NULL
);

-- =========================================================
-- ESTRUTURA FLEXÍVEL DE RELATÓRIOS
-- =========================================================

CREATE TABLE report_templates (
    id TEXT PRIMARY KEY,
    empresa_id TEXT REFERENCES empresas(id),
    report_type_id TEXT NOT NULL REFERENCES report_types(id),
    name TEXT NOT NULL,
    is_default INTEGER DEFAULT 0,
    created_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE report_template_lines (
    id TEXT PRIMARY KEY,
    template_id TEXT NOT NULL REFERENCES report_templates(id),
    parent_id TEXT REFERENCES report_template_lines(id),
    line_order INTEGER NOT NULL,
    code TEXT,
    title TEXT NOT NULL,
    line_type TEXT NOT NULL,
    formula TEXT,
    is_bold INTEGER DEFAULT 0,
    created_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE report_line_accounts (
    id TEXT PRIMARY KEY,
    report_line_id TEXT NOT NULL REFERENCES report_template_lines(id),
    conta_id TEXT NOT NULL REFERENCES plano_contas(id)
);

CREATE TABLE mapa_demonstracoes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  conta_id INTEGER,
  tipo TEXT,
  categoria TEXT,
  excluido_at TEXT,
  FOREIGN KEY (conta_id) REFERENCES plano_contas(id)
);

CREATE INDEX idx_lancamento_data ON lancamento(data);
CREATE INDEX idx_lancamento_item_conta ON lancamento_item(conta_id);

-- =========================================================
-- TAGS CONTÁBEIS
-- =========================================================

CREATE TABLE tags (
    id TEXT PRIMARY KEY,
    empresa_id TEXT REFERENCES empresas(id),
    name TEXT NOT NULL
);

CREATE TABLE lancamento_item_tags (
    lancamento_item_id TEXT REFERENCES lancamento_item(id),
    tag_id TEXT REFERENCES tags(id),
    PRIMARY KEY (lancamento_item_id, tag_id)
);

-- =========================================================
-- DE-PARA SPED
-- =========================================================

CREATE TABLE sped_mappings (
    id TEXT PRIMARY KEY,
    conta_id TEXT NOT NULL REFERENCES plano_contas(id),
    sped_code TEXT NOT NULL,
    description TEXT
);

-- Converted extension: CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- =========================================================
-- USUÁRIOS
-- =========================================================

CREATE TABLE usuarios (
    id TEXT PRIMARY KEY,
    nome TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    is_active INTEGER DEFAULT 1,
    last_login_at TEXT,
    created_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE regras (
    id TEXT PRIMARY KEY,
    code TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL
);

INSERT INTO regras (id, code, name)
VALUES
(lower(hex(randomblob(16))), 'SUPER_ADMIN', 'Super Administrador'),
(lower(hex(randomblob(16))), 'ACCOUNTANT', 'Contador'),
(lower(hex(randomblob(16))), 'ASSISTANT', 'Assistente Contábil'),
(lower(hex(randomblob(16))), 'AUDITOR', 'Auditor'),
(lower(hex(randomblob(16))), 'CLIENT', 'Cliente');

CREATE TABLE permissoes (
    id TEXT PRIMARY KEY,
    code TEXT UNIQUE NOT NULL,
    descricao TEXT
);

INSERT INTO permissoes (id, code, descricao)
VALUES
(lower(hex(randomblob(16))), 'COMPANY_VIEW', 'Visualizar empresas'),
(lower(hex(randomblob(16))), 'COMPANY_EDIT', 'Editar empresas'),
(lower(hex(randomblob(16))), 'ACCOUNT_VIEW', 'Visualizar plano de contas'),
(lower(hex(randomblob(16))), 'ACCOUNT_EDIT', 'Editar plano de contas'),
(lower(hex(randomblob(16))), 'ENTRY_VIEW', 'Visualizar lançamentos'),
(lower(hex(randomblob(16))), 'ENTRY_CREATE', 'Criar lançamentos'),
(lower(hex(randomblob(16))), 'ENTRY_EDIT', 'Editar lançamentos'),
(lower(hex(randomblob(16))), 'REPORT_VIEW', 'Visualizar relatórios'),
(lower(hex(randomblob(16))), 'REPORT_EDIT', 'Editar relatórios'),
(lower(hex(randomblob(16))), 'SPED_EXPORT', 'Exportar SPED'),
(lower(hex(randomblob(16))), 'ECD_SIGN', 'Assinar ECD');

CREATE TABLE regra_permissao (
    role_id TEXT REFERENCES regras(id),
    permission_id TEXT REFERENCES permissoes(id),
    PRIMARY KEY (role_id, permission_id)
);

CREATE TABLE empresa_usuario (
    user_id TEXT REFERENCES usuarios(id),
    company_id TEXT REFERENCES empresas(id),
    role_id TEXT REFERENCES regras(id),
    PRIMARY KEY (user_id, company_id)
);

CREATE TABLE usuario_sessoes (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES usuarios(id),
    token TEXT NOT NULL UNIQUE,
    ip_address TEXT,
    user_agent TEXT,
    expires_at TEXT NOT NULL,
    revoked INTEGER DEFAULT 0,
    created_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE audit_logs (
    id TEXT PRIMARY KEY,
    company_id TEXT REFERENCES empresas(id),
    user_id TEXT REFERENCES usuarios(id),
    entity_name TEXT,
    entity_id TEXT,
    action TEXT,
    old_data TEXT,
    new_data TEXT,
    created_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE sped_natureza (
    id TEXT PRIMARY KEY,
    code TEXT UNIQUE NOT NULL,
    description TEXT NOT NULL
);

INSERT INTO sped_natureza (id, code, description)
VALUES
(lower(hex(randomblob(16))), '01', 'Contas de Ativo'),
(lower(hex(randomblob(16))), '02', 'Contas de Passivo'),
(lower(hex(randomblob(16))), '03', 'Patrimônio Líquido'),
(lower(hex(randomblob(16))), '04', 'Receitas'),
(lower(hex(randomblob(16))), '05', 'Custos'),
(lower(hex(randomblob(16))), '06', 'Despesas');

-- ALTER TABLE ADD COLUMN statements are not directly supported in the same manner in SQLite
-- The following column definition is preserved for manual migration if needed:
-- ALTER TABLE company_accounts ADD COLUMN sped_nature_id TEXT REFERENCES sped_natureza(id);

CREATE TABLE report_versions (
    id TEXT PRIMARY KEY,
    empresa_id TEXT NOT NULL REFERENCES empresas(id),
    report_template_id TEXT REFERENCES report_templates(id),
    report_type_id TEXT REFERENCES report_types(id),
    version_number INTEGER NOT NULL,
    fiscal_year INTEGER NOT NULL,
    start_period TEXT NOT NULL,
    end_period TEXT NOT NULL,
    generated_by TEXT REFERENCES users(id),
    is_locked INTEGER DEFAULT 0,
    notes TEXT,
    created_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE report_version_lines (
    id TEXT PRIMARY KEY,
    report_version_id TEXT NOT NULL REFERENCES report_versions(id),
    line_order INTEGER,
    code TEXT,
    title TEXT,
    amount NUMERIC(18,2),
    created_at TEXT DEFAULT (datetime('now'))
);

-- ALTER TABLE report_versions ADD COLUMN integrity_hash TEXT;

CREATE TABLE trava_contabil (
    id TEXT PRIMARY KEY,
    empresa_id TEXT NOT NULL REFERENCES empresas(id),
    year INTEGER NOT NULL,
    month INTEGER NOT NULL,
    is_closed INTEGER DEFAULT 0,
    closed_by TEXT REFERENCES usuarios(id),
    closed_at TEXT
);

CREATE TABLE certificados_digitais (
    id TEXT PRIMARY KEY,
    empresa_id TEXT NOT NULL REFERENCES empresas(id),
    certificate_name TEXT,
    serial_number TEXT,
    valid_from TEXT,
    valid_until TEXT,
    issuer TEXT,
    encrypted_pfx BLOB,
    created_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE ecd_arquivos (
    id TEXT PRIMARY KEY,
    empresa_id TEXT NOT NULL REFERENCES empresas(id),
    fiscal_year INTEGER NOT NULL,
    file_name TEXT,
    file_hash TEXT,
    generated_by TEXT REFERENCES usuarios(id),
    generated_at TEXT DEFAULT (datetime('now')),
    signed_at TEXT,
    delivered_at TEXT,
    status TEXT
);

CREATE TABLE assinaturas_digitais (
    id TEXT PRIMARY KEY,
    ecd_file_id TEXT NOT NULL REFERENCES ecd_files(id),
    signed_by TEXT REFERENCES usuarios(id),
    certificate_id TEXT REFERENCES digital_certificates(id),
    signature_hash TEXT NOT NULL,
    signed_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE sped_entregas (
    id TEXT PRIMARY KEY,
    empresa_id TEXT NOT NULL REFERENCES empresas(id),
    sped_type TEXT,
    fiscal_year INTEGER,
    protocol TEXT,
    receipt_number TEXT,
    delivered_at TEXT,
    status TEXT
);

CREATE TABLE jobs (
    id TEXT PRIMARY KEY,
    queue_name TEXT,
    payload TEXT,
    status TEXT DEFAULT 'PENDING',
    retries INTEGER DEFAULT 0,
    created_at TEXT DEFAULT (datetime('now')),
    processed_at TEXT
);

CREATE VIEW user_permissions_view AS
SELECT
    uc.user_id,
    uc.empresa_id,
    p.code AS permission_code
FROM empresa_usuario uc
JOIN regra_permissao rp
    ON rp.role_id = uc.role_id
JOIN permissoes p
    ON p.id = rp.permission_id;

CREATE VIEW trial_balance_view AS
SELECT
    a.id,
    a.code,
    a.name,
    SUM(l.debit) AS total_debit,
    SUM(l.credit) AS total_credit,
    SUM(l.debit - l.credit) AS balance
FROM plano_contas a
LEFT JOIN lancamento_item l
    ON l.conta_id = a.id
GROUP BY
    a.id,
    a.code,
    a.name;

CREATE TABLE empresa_configuracao (
    empresa_id TEXT PRIMARY KEY REFERENCES companies(id),
    permitir_dinheiro_negativo INTEGER DEFAULT 0,
    periodo_fechamento_automatico INTEGER DEFAULT 0,
    default_report_template TEXT REFERENCES report_templates(id),
    created_at TEXT DEFAULT (datetime('now'))
);
