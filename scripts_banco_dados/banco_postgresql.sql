-- =========================================================
-- CONTABILIDADE - BANCO DE DADOS PostgreSQL
-- Convertido de SQLite3 (banco_sqlite3_novo.sql)
-- =========================================================

-- Necessário para gen_random_uuid() em versões < PostgreSQL 13
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- =========================================================
-- EMPRESAS
-- =========================================================

CREATE TABLE empresa (
  id BIGSERIAL PRIMARY KEY,
  cnpj TEXT NOT NULL,
  nome TEXT NOT NULL,
  uf TEXT,
  municipio TEXT,
  data_inicio DATE,
  data_fim DATE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  excluido_at TIMESTAMP WITH TIME ZONE
);

-- =========================================================
-- TIPOS DE DEMONSTRAÇÕES
-- =========================================================

CREATE TABLE report_types (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    code VARCHAR(30) UNIQUE NOT NULL,
    name TEXT NOT NULL
);

INSERT INTO report_types (code, name)
VALUES
('BALANCO', 'Balanço Patrimonial'),
('DRE', 'Demonstração do Resultado'),
('DFC', 'Demonstração do Fluxo de Caixa'),
('DVA', 'Demonstração do Valor Adicionado'),
('BALANCETE', 'Balancete');

-- =========================================================
-- PLANO DE CONTAS REFERENCIAL
-- =========================================================

CREATE TABLE plano_contas_referencial (
    id BIGSERIAL PRIMARY KEY,
    codigo TEXT NOT NULL,
    nome TEXT NOT NULL,
    tipo TEXT,
    natureza TEXT,
    nivel INTEGER,
    parent_id BIGINT REFERENCES plano_contas_referencial(id),
    grupo TEXT,
    dre_grupo TEXT,
    fluxo_caixa_tipo TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    excluded_at TIMESTAMP WITH TIME ZONE
);

-- =========================================================
-- PLANO DE CONTAS POR EMPRESA
-- =========================================================

CREATE TABLE plano_contas (
  id BIGSERIAL PRIMARY KEY,
  empresa_id BIGINT REFERENCES empresa(id),
  plano_contas_referencial_id BIGINT REFERENCES plano_contas_referencial(id),
  codigo TEXT NOT NULL,
  descricao TEXT NOT NULL,
  tipo TEXT NOT NULL,
  natureza TEXT,
  nivel INTEGER NOT NULL,
  conta_pai_id BIGINT REFERENCES plano_contas(id),
  codigo_referencial TEXT,
  aceita_lancamento BOOLEAN DEFAULT TRUE,
  grupo TEXT,
  subgrupo TEXT,
  dre_grupo TEXT,
  fluxo_caixa_tipo TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  excluido_at TIMESTAMP WITH TIME ZONE
);

-- =========================================================
-- CENTRO DE CUSTO
-- =========================================================

CREATE TABLE centro_custo (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    empresa_id BIGINT NOT NULL REFERENCES empresa(id),
    codigo TEXT,
    nome TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =========================================================
-- LANÇAMENTOS
-- =========================================================

CREATE TABLE lancamento (
  id BIGSERIAL PRIMARY KEY,
  empresa_id BIGINT REFERENCES empresa(id),
  data DATE NOT NULL,
  historico TEXT,
  tipo TEXT DEFAULT 'N',
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  excluido_at TIMESTAMP WITH TIME ZONE
);

CREATE TABLE lancamento_item (
  id BIGSERIAL PRIMARY KEY,
  lancamento_id BIGINT REFERENCES lancamento(id) ON DELETE CASCADE,
  conta_id BIGINT REFERENCES plano_contas(id),
  centro_custo_id UUID REFERENCES centro_custo(id),
  tipo TEXT NOT NULL,
  valor NUMERIC(14,2) NOT NULL
);

-- =========================================================
-- ESTRUTURA FLEXÍVEL DE RELATÓRIOS
-- =========================================================

CREATE TABLE report_templates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    empresa_id BIGINT REFERENCES empresa(id),
    report_type_id UUID NOT NULL REFERENCES report_types(id),
    name TEXT NOT NULL,
    is_default BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE report_template_lines (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    template_id UUID NOT NULL REFERENCES report_templates(id),
    parent_id UUID REFERENCES report_template_lines(id),
    line_order INTEGER NOT NULL,
    code TEXT,
    title TEXT NOT NULL,
    line_type TEXT NOT NULL,
    formula TEXT,
    is_bold BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE report_line_accounts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    report_line_id UUID NOT NULL REFERENCES report_template_lines(id),
    conta_id BIGINT NOT NULL REFERENCES plano_contas(id)
);

CREATE TABLE mapa_demonstracoes (
  id BIGSERIAL PRIMARY KEY,
  conta_id BIGINT REFERENCES plano_contas(id),
  tipo TEXT,
  categoria TEXT,
  excluido_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_lancamento_data ON lancamento(data);
CREATE INDEX idx_lancamento_item_conta ON lancamento_item(conta_id);

-- =========================================================
-- TAGS CONTÁBEIS
-- =========================================================

CREATE TABLE tags (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    empresa_id BIGINT REFERENCES empresa(id),
    name TEXT NOT NULL
);

CREATE TABLE lancamento_item_tags (
    lancamento_item_id BIGINT REFERENCES lancamento_item(id),
    tag_id UUID REFERENCES tags(id),
    PRIMARY KEY (lancamento_item_id, tag_id)
);

-- =========================================================
-- DE-PARA SPED
-- =========================================================

CREATE TABLE sped_mappings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conta_id BIGINT NOT NULL REFERENCES plano_contas(id),
    sped_code TEXT NOT NULL,
    description TEXT
);

-- =========================================================
-- USUÁRIOS E PERMISSÕES
-- =========================================================

CREATE TABLE usuarios (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    last_login_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE regras (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    code TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL
);

INSERT INTO regras (code, name)
VALUES
('SUPER_ADMIN', 'Super Administrador'),
('ACCOUNTANT', 'Contador'),
('ASSISTANT', 'Assistente Contábil'),
('AUDITOR', 'Auditor'),
('CLIENT', 'Cliente');

CREATE TABLE permissoes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    code TEXT UNIQUE NOT NULL,
    descricao TEXT
);

INSERT INTO permissoes (code, descricao)
VALUES
('COMPANY_VIEW', 'Visualizar empresas'),
('COMPANY_EDIT', 'Editar empresas'),
('ACCOUNT_VIEW', 'Visualizar plano de contas'),
('ACCOUNT_EDIT', 'Editar plano de contas'),
('ENTRY_VIEW', 'Visualizar lançamentos'),
('ENTRY_CREATE', 'Criar lançamentos'),
('ENTRY_EDIT', 'Editar lançamentos'),
('REPORT_VIEW', 'Visualizar relatórios'),
('REPORT_EDIT', 'Editar relatórios'),
('SPED_EXPORT', 'Exportar SPED'),
('ECD_SIGN', 'Assinar ECD');

CREATE TABLE regra_permissao (
    role_id UUID REFERENCES regras(id),
    permission_id UUID REFERENCES permissoes(id),
    PRIMARY KEY (role_id, permission_id)
);

CREATE TABLE empresa_usuario (
    user_id UUID REFERENCES usuarios(id),
    company_id BIGINT REFERENCES empresa(id),
    role_id UUID REFERENCES regras(id),
    PRIMARY KEY (user_id, company_id)
);

CREATE TABLE usuario_sessoes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES usuarios(id),
    token TEXT NOT NULL UNIQUE,
    ip_address INET,
    user_agent TEXT,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    revoked BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id BIGINT REFERENCES empresa(id),
    user_id UUID REFERENCES usuarios(id),
    entity_name TEXT,
    entity_id TEXT,
    action TEXT,
    old_data JSONB,
    new_data JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =========================================================
-- NATUREZA SPED
-- =========================================================

CREATE TABLE sped_natureza (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    code TEXT UNIQUE NOT NULL,
    description TEXT NOT NULL
);

INSERT INTO sped_natureza (code, description)
VALUES
('01', 'Contas de Ativo'),
('02', 'Contas de Passivo'),
('03', 'Patrimônio Líquido'),
('04', 'Receitas'),
('05', 'Custos'),
('06', 'Despesas');

-- =========================================================
-- VERSÕES DE RELATÓRIOS
-- =========================================================

CREATE TABLE report_versions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    empresa_id BIGINT NOT NULL REFERENCES empresa(id),
    report_template_id UUID REFERENCES report_templates(id),
    report_type_id UUID REFERENCES report_types(id),
    version_number INTEGER NOT NULL,
    fiscal_year INTEGER NOT NULL,
    start_period DATE NOT NULL,
    end_period DATE NOT NULL,
    generated_by UUID REFERENCES usuarios(id),
    is_locked BOOLEAN DEFAULT FALSE,
    notes TEXT,
    integrity_hash TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE report_version_lines (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    report_version_id UUID NOT NULL REFERENCES report_versions(id),
    line_order INTEGER,
    code TEXT,
    title TEXT,
    amount NUMERIC(18,2),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =========================================================
-- TRAVA CONTÁBIL
-- =========================================================

CREATE TABLE trava_contabil (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    empresa_id BIGINT NOT NULL REFERENCES empresa(id),
    year INTEGER NOT NULL,
    month INTEGER NOT NULL,
    is_closed BOOLEAN DEFAULT FALSE,
    closed_by UUID REFERENCES usuarios(id),
    closed_at TIMESTAMP WITH TIME ZONE
);

-- =========================================================
-- CERTIFICADOS DIGITAIS
-- =========================================================

CREATE TABLE certificados_digitais (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    empresa_id BIGINT NOT NULL REFERENCES empresa(id),
    certificate_name TEXT,
    serial_number TEXT,
    valid_from DATE,
    valid_until DATE,
    issuer TEXT,
    encrypted_pfx BYTEA,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =========================================================
-- ECD
-- =========================================================

CREATE TABLE ecd_arquivos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    empresa_id BIGINT NOT NULL REFERENCES empresa(id),
    fiscal_year INTEGER NOT NULL,
    file_name TEXT,
    file_hash TEXT,
    generated_by UUID REFERENCES usuarios(id),
    generated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    signed_at TIMESTAMP WITH TIME ZONE,
    delivered_at TIMESTAMP WITH TIME ZONE,
    status TEXT
);

CREATE TABLE assinaturas_digitais (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ecd_file_id UUID NOT NULL REFERENCES ecd_arquivos(id),
    signed_by UUID REFERENCES usuarios(id),
    certificate_id UUID REFERENCES certificados_digitais(id),
    signature_hash TEXT NOT NULL,
    signed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =========================================================
-- SPED ENTREGAS
-- =========================================================

CREATE TABLE sped_entregas (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    empresa_id BIGINT NOT NULL REFERENCES empresa(id),
    sped_type TEXT,
    fiscal_year INTEGER,
    protocol TEXT,
    receipt_number TEXT,
    delivered_at TIMESTAMP WITH TIME ZONE,
    status TEXT
);

-- =========================================================
-- JOBS
-- =========================================================

CREATE TABLE jobs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    queue_name TEXT,
    payload JSONB,
    status TEXT DEFAULT 'PENDING',
    retries INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    processed_at TIMESTAMP WITH TIME ZONE
);

-- =========================================================
-- CONFIGURAÇÃO DE EMPRESA
-- =========================================================

CREATE TABLE empresa_configuracao (
    empresa_id BIGINT PRIMARY KEY REFERENCES empresa(id),
    permitir_dinheiro_negativo BOOLEAN DEFAULT FALSE,
    periodo_fechamento_automatico BOOLEAN DEFAULT FALSE,
    default_report_template UUID REFERENCES report_templates(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =========================================================
-- VIEWS
-- =========================================================

CREATE VIEW user_permissions_view AS
SELECT
    uc.user_id,
    uc.company_id AS empresa_id,
    p.code AS permission_code
FROM empresa_usuario uc
JOIN regra_permissao rp
    ON rp.role_id = uc.role_id
JOIN permissoes p
    ON p.id = rp.permission_id;

CREATE VIEW trial_balance_view AS
SELECT
    a.id,
    a.codigo AS code,
    a.descricao AS name,
    SUM(CASE WHEN li.tipo = 'D' THEN li.valor ELSE 0 END) AS total_debit,
    SUM(CASE WHEN li.tipo = 'C' THEN li.valor ELSE 0 END) AS total_credit,
    SUM(CASE WHEN li.tipo = 'D' THEN li.valor ELSE -li.valor END) AS balance
FROM plano_contas a
LEFT JOIN lancamento_item li
    ON li.conta_id = a.id
GROUP BY
    a.id,
    a.codigo,
    a.descricao;
