-- =========================================================
-- ESTRUTURA CONTÁBIL FLEXÍVEL E ESCALÁVEL
-- Plano de contas referencial + plano por empresa
-- Compatível com:
-- - Balanço
-- - DRE
-- - DFC
-- - DVA
-- - Balancete
-- - SPED
-- - Relatórios customizados
-- =========================================================

-- PostgreSQL
-- =========================================================



-- =========================================================
-- EMPRESAS
-- =========================================================

CREATE TABLE companies (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    legal_name VARCHAR(255) NOT NULL,
    trade_name VARCHAR(255),
    document VARCHAR(20) NOT NULL,
    tax_regime VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW()
);



-- =========================================================
-- TIPOS DE DEMONSTRAÇÕES
-- =========================================================

CREATE TABLE report_types (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    code VARCHAR(30) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL
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
-- MODELO BASE DO SISTEMA
-- =========================================================

CREATE TABLE chart_of_accounts_reference (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    parent_id UUID REFERENCES chart_of_accounts_reference(id),

    code VARCHAR(30) NOT NULL,
    name VARCHAR(255) NOT NULL,

    account_type VARCHAR(30) NOT NULL,
    -- ASSET
    -- LIABILITY
    -- EQUITY
    -- REVENUE
    -- COST
    -- EXPENSE

    level INT NOT NULL DEFAULT 1,

    accepts_entries BOOLEAN DEFAULT FALSE,

    is_active BOOLEAN DEFAULT TRUE,
    
    tipo VARCHAR(1), -- A - Analitica, S - Sintetica
    
    natureza VARCHAR(1), -- natureza da conta : D - Devedora, C - Credora
    
    nivel INT, -- Profundidade da conta na árvore (ex: 1 = contas raiz, 2 = subgrupos, 3 = contas analíticas). Usado para indentação visual.
    
    grupo VARCHAR(10),
--  Classificação no Balanço Patrimonial:
--  - `ATIVO`: bens e direitos
--  - `PASSIVO`: obrigações
--  - `PL`: patrimônio líquido
    
    dre_grupo VARCHAR(10),
--  Classificação na Demonstração do Resultado (DRE):
--  - `RECEITA_BRUTA`: receitas operacionais
--  - `CUSTO`: custo dos produtos vendidos
--  - `DESPESA_OPERACIONAL`: despesas gerais
--  - `RESULTADO_FINANCEIRO`: juros e variações financeiras
    
    fluxo_caixa_tipo VARCHAR(10), 
--  Classificação no Fluxo de Caixa (DFC):
--  - `OPERACIONAL`: atividades operacionais
--  - `INVESTIMENTO`: compra/venda de ativos
--  - `FINANCIAMENTO`: empréstimos e dividendos   
    
    created_at TIMESTAMP DEFAULT NOW()
);



-- =========================================================
-- EXEMPLO DE CONTAS REFERENCIAIS
-- =========================================================

INSERT INTO chart_of_accounts_reference
(code, name, account_type, level, accepts_entries)
VALUES
('1', 'ATIVO', 'ASSET', 1, FALSE),
('1.1', 'ATIVO CIRCULANTE', 'ASSET', 2, FALSE),
('1.1.01', 'CAIXA E EQUIVALENTES', 'ASSET', 3, FALSE),
('1.1.01.001', 'CAIXA', 'ASSET', 4, TRUE),

('2', 'PASSIVO', 'LIABILITY', 1, FALSE),

('3', 'PATRIMÔNIO LÍQUIDO', 'EQUITY', 1, FALSE),

('4', 'RECEITAS', 'REVENUE', 1, FALSE),
('4.1', 'RECEITAS OPERACIONAIS', 'REVENUE', 2, FALSE),

('5', 'CUSTOS', 'COST', 1, FALSE),

('6', 'DESPESAS', 'EXPENSE', 1, FALSE);



-- =========================================================
-- PLANO DE CONTAS DA EMPRESA
-- CADA EMPRESA PODE:
-- - HERDAR
-- - RENOMEAR
-- - CRIAR NOVAS CONTAS
-- =========================================================

CREATE TABLE company_accounts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    company_id UUID NOT NULL REFERENCES companies(id),

    reference_account_id UUID
        REFERENCES chart_of_accounts_reference(id),

    parent_id UUID REFERENCES company_accounts(id),

    code VARCHAR(30) NOT NULL,
    name VARCHAR(255) NOT NULL,

    account_type VARCHAR(30) NOT NULL,

    level INT NOT NULL DEFAULT 1,

    accepts_entries BOOLEAN DEFAULT FALSE,

    is_system BOOLEAN DEFAULT FALSE,
    -- TRUE = veio do plano referencial
    -- FALSE = criado pelo contador

    is_active BOOLEAN DEFAULT TRUE,

    created_at TIMESTAMP DEFAULT NOW()
);



-- =========================================================
-- CENTRO DE CUSTO
-- =========================================================

CREATE TABLE cost_centers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    company_id UUID NOT NULL REFERENCES companies(id),

    code VARCHAR(30),
    name VARCHAR(255) NOT NULL,

    created_at TIMESTAMP DEFAULT NOW()
);



-- =========================================================
-- LANÇAMENTOS CONTÁBEIS
-- =========================================================

CREATE TABLE journal_entries (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    company_id UUID NOT NULL REFERENCES companies(id),

    entry_date DATE NOT NULL,

    description TEXT,

    created_at TIMESTAMP DEFAULT NOW()
);



CREATE TABLE journal_entry_lines (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    journal_entry_id UUID NOT NULL
        REFERENCES journal_entries(id),

    account_id UUID NOT NULL
        REFERENCES company_accounts(id),

    cost_center_id UUID
        REFERENCES cost_centers(id),

    debit NUMERIC(18,2) DEFAULT 0,
    credit NUMERIC(18,2) DEFAULT 0,

    history TEXT
);



-- =========================================================
-- ESTRUTURA FLEXÍVEL DE RELATÓRIOS
-- AQUI ESTÁ A PARTE IMPORTANTE
-- =========================================================

CREATE TABLE report_templates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    company_id UUID REFERENCES companies(id),
    -- NULL = template global

    report_type_id UUID NOT NULL
        REFERENCES report_types(id),

    name VARCHAR(255) NOT NULL,

    is_default BOOLEAN DEFAULT FALSE,

    created_at TIMESTAMP DEFAULT NOW()
);



-- =========================================================
-- LINHAS DO RELATÓRIO
-- DEFINE:
-- - ORDEM
-- - AGRUPAMENTOS
-- - FÓRMULAS
-- - CONTAS
-- =========================================================

CREATE TABLE report_template_lines (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    template_id UUID NOT NULL
        REFERENCES report_templates(id),

    parent_id UUID
        REFERENCES report_template_lines(id),

    line_order INT NOT NULL,

    code VARCHAR(50),

    title VARCHAR(255) NOT NULL,

    line_type VARCHAR(30) NOT NULL,
    -- GROUP
    -- ACCOUNT
    -- FORMULA

    formula TEXT,

    is_bold BOOLEAN DEFAULT FALSE,

    created_at TIMESTAMP DEFAULT NOW()
);



-- =========================================================
-- RELACIONAMENTO:
-- LINHA DO RELATÓRIO -> CONTAS CONTÁBEIS
-- =========================================================

CREATE TABLE report_line_accounts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    report_line_id UUID NOT NULL
        REFERENCES report_template_lines(id),

    account_id UUID NOT NULL
        REFERENCES company_accounts(id)
);



-- =========================================================
-- EXEMPLO DE DRE CUSTOMIZADA
-- =========================================================

-- RECEITA BRUTA
-- (-) IMPOSTOS
-- (=) RECEITA LÍQUIDA
-- (-) DESPESAS OPERACIONAIS
-- (=) EBITDA
-- (-) DEPRECIAÇÃO
-- (=) EBIT
-- (-) FINANCEIRO
-- (=) LUCRO LÍQUIDO



-- =========================================================
-- TAGS CONTÁBEIS
-- MUITO ÚTIL PARA SAAS MODERNO
-- =========================================================

CREATE TABLE tags (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    company_id UUID REFERENCES companies(id),

    name VARCHAR(100) NOT NULL
);



CREATE TABLE journal_entry_line_tags (
    line_id UUID REFERENCES journal_entry_lines(id),
    tag_id UUID REFERENCES tags(id),

    PRIMARY KEY (line_id, tag_id)
);



-- =========================================================
-- DE-PARA SPED
-- =========================================================

CREATE TABLE sped_mappings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    account_id UUID NOT NULL
        REFERENCES company_accounts(id),

    sped_code VARCHAR(50) NOT NULL,

    description VARCHAR(255)
);



-- =========================================================
-- VISÃO DE BALANCETE
-- =========================================================

CREATE VIEW trial_balance_view AS
SELECT
    a.id,
    a.code,
    a.name,

    SUM(l.debit) AS total_debit,
    SUM(l.credit) AS total_credit,

    SUM(l.debit - l.credit) AS balance

FROM company_accounts a

LEFT JOIN journal_entry_lines l
    ON l.account_id = a.id

GROUP BY
    a.id,
    a.code,
    a.name;



-- =========================================================
-- EXEMPLO DE CONSULTA DRE
-- =========================================================

/*

SELECT
    rtl.title,
    SUM(jel.credit - jel.debit) AS amount

FROM report_template_lines rtl

JOIN report_line_accounts rla
    ON rla.report_line_id = rtl.id

JOIN journal_entry_lines jel
    ON jel.account_id = rla.account_id

GROUP BY rtl.title
ORDER BY rtl.line_order;

*/



-- =========================================================
-- IDEIA ARQUITETURAL IMPORTANTE
-- =========================================================

/*

O RELATÓRIO NÃO DEPENDE DO PLANO DE CONTAS.

Essa é a chave.

Você pode:

- alterar a DRE sem alterar contas;
- criar DRE gerencial;
- criar DRE fiscal;
- criar DRE bancária;
- criar DRE médica;
- criar balanço resumido;
- criar balanço analítico;
- criar DFC indireta;
- criar DFC direta.

Tudo apenas remapeando:
report_template_lines
+
report_line_accounts

Isso é exatamente como ERPs modernos funcionam.

*/




-- =========================================================
-- SUGESTÕES FUTURAS
-- =========================================================

/*

1. Natureza SPED
2. Multi-filial
3. Multi-moeda
4. Consolidação empresarial
5. Versionamento de demonstrações
6. Assinatura digital ECD
7. Motor de fórmulas
8. Indicadores automáticos
9. Inteligência contábil
10. Regras automáticas de classificação

*/

-- =========================================================
-- CONTINUAÇÃO DA ARQUITETURA CONTÁBIL
-- CONTROLE DE ACESSO + SPED + VERSIONAMENTO + ECD
-- PostgreSQL
-- =========================================================



-- =========================================================
-- EXTENSÕES NECESSÁRIAS
-- =========================================================

CREATE EXTENSION IF NOT EXISTS "pgcrypto";



-- =========================================================
-- USUÁRIOS
-- =========================================================

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    full_name VARCHAR(255) NOT NULL,

    email VARCHAR(255) UNIQUE NOT NULL,

    password_hash TEXT NOT NULL,

    is_active BOOLEAN DEFAULT TRUE,

    last_login_at TIMESTAMP,

    created_at TIMESTAMP DEFAULT NOW()
);



-- =========================================================
-- PERFIS DE ACESSO
-- =========================================================

CREATE TABLE roles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    code VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL
);



INSERT INTO roles (code, name)
VALUES
('SUPER_ADMIN', 'Super Administrador'),
('ACCOUNTANT', 'Contador'),
('ASSISTANT', 'Assistente Contábil'),
('AUDITOR', 'Auditor'),
('CLIENT', 'Cliente');



-- =========================================================
-- PERMISSÕES
-- =========================================================

CREATE TABLE permissions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    code VARCHAR(100) UNIQUE NOT NULL,
    description VARCHAR(255)
);



INSERT INTO permissions (code, description)
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



-- =========================================================
-- ROLE -> PERMISSIONS
-- =========================================================

CREATE TABLE role_permissions (
    role_id UUID REFERENCES roles(id),
    permission_id UUID REFERENCES permissions(id),

    PRIMARY KEY (role_id, permission_id)
);



-- =========================================================
-- USUÁRIO -> EMPRESA
-- MULTIEMPRESA
-- =========================================================

CREATE TABLE user_companies (
    user_id UUID REFERENCES users(id),

    company_id UUID REFERENCES companies(id),

    role_id UUID REFERENCES roles(id),

    PRIMARY KEY (user_id, company_id)
);



-- =========================================================
-- SESSÕES / LOGIN
-- =========================================================

CREATE TABLE user_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    user_id UUID NOT NULL REFERENCES users(id),

    token TEXT NOT NULL UNIQUE,

    ip_address VARCHAR(100),

    user_agent TEXT,

    expires_at TIMESTAMP NOT NULL,

    revoked BOOLEAN DEFAULT FALSE,

    created_at TIMESTAMP DEFAULT NOW()
);



-- =========================================================
-- AUDITORIA
-- =========================================================

CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    company_id UUID REFERENCES companies(id),

    user_id UUID REFERENCES users(id),

    entity_name VARCHAR(100),

    entity_id UUID,

    action VARCHAR(50),
    -- INSERT
    -- UPDATE
    -- DELETE
    -- LOGIN
    -- LOGOUT

    old_data JSONB,

    new_data JSONB,

    created_at TIMESTAMP DEFAULT NOW()
);



-- =========================================================
-- ITEM 1
-- NATUREZA SPED
-- =========================================================

CREATE TABLE sped_account_natures (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    code VARCHAR(20) UNIQUE NOT NULL,

    description VARCHAR(255) NOT NULL
);



INSERT INTO sped_account_natures (code, description)
VALUES
('01', 'Contas de Ativo'),
('02', 'Contas de Passivo'),
('03', 'Patrimônio Líquido'),
('04', 'Receitas'),
('05', 'Custos'),
('06', 'Despesas');



ALTER TABLE company_accounts
ADD COLUMN sped_nature_id UUID
REFERENCES sped_account_natures(id);



-- =========================================================
-- ITEM 5
-- VERSIONAMENTO DE DEMONSTRAÇÕES
-- =========================================================

CREATE TABLE report_versions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    company_id UUID NOT NULL REFERENCES companies(id),

    report_template_id UUID
        REFERENCES report_templates(id),

    report_type_id UUID
        REFERENCES report_types(id),

    version_number INT NOT NULL,

    fiscal_year INT NOT NULL,

    start_period DATE NOT NULL,
    end_period DATE NOT NULL,

    generated_by UUID REFERENCES users(id),

    is_locked BOOLEAN DEFAULT FALSE,

    notes TEXT,

    created_at TIMESTAMP DEFAULT NOW()
);



-- =========================================================
-- SNAPSHOT DAS LINHAS
-- GUARDA O RELATÓRIO COMO FOI GERADO
-- =========================================================

CREATE TABLE report_version_lines (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    report_version_id UUID NOT NULL
        REFERENCES report_versions(id),

    line_order INT,

    code VARCHAR(50),

    title VARCHAR(255),

    amount NUMERIC(18,2),

    created_at TIMESTAMP DEFAULT NOW()
);



-- =========================================================
-- HASH DE INTEGRIDADE
-- =========================================================

ALTER TABLE report_versions
ADD COLUMN integrity_hash TEXT;



-- =========================================================
-- TRAVA CONTÁBIL
-- EVITA ALTERAÇÃO APÓS FECHAMENTO
-- =========================================================

CREATE TABLE accounting_periods (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    company_id UUID NOT NULL REFERENCES companies(id),

    year INT NOT NULL,
    month INT NOT NULL,

    is_closed BOOLEAN DEFAULT FALSE,

    closed_by UUID REFERENCES users(id),

    closed_at TIMESTAMP
);



-- =========================================================
-- ITEM 6
-- ASSINATURA DIGITAL ECD
-- =========================================================

CREATE TABLE digital_certificates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    company_id UUID NOT NULL REFERENCES companies(id),

    certificate_name VARCHAR(255),

    serial_number VARCHAR(255),

    valid_from DATE,
    valid_until DATE,

    issuer VARCHAR(255),

    encrypted_pfx BYTEA,

    created_at TIMESTAMP DEFAULT NOW()
);



-- =========================================================
-- ARQUIVOS ECD GERADOS
-- =========================================================

CREATE TABLE ecd_files (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    company_id UUID NOT NULL REFERENCES companies(id),

    fiscal_year INT NOT NULL,

    file_name VARCHAR(255),

    file_hash TEXT,

    generated_by UUID REFERENCES users(id),

    generated_at TIMESTAMP DEFAULT NOW(),

    signed_at TIMESTAMP,

    delivered_at TIMESTAMP,

    status VARCHAR(50)
    -- GENERATED
    -- SIGNED
    -- DELIVERED
    -- REJECTED
);



-- =========================================================
-- ASSINATURAS DIGITAIS
-- =========================================================

CREATE TABLE digital_signatures (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    ecd_file_id UUID NOT NULL
        REFERENCES ecd_files(id),

    signed_by UUID REFERENCES users(id),

    certificate_id UUID
        REFERENCES digital_certificates(id),

    signature_hash TEXT NOT NULL,

    signed_at TIMESTAMP DEFAULT NOW()
);



-- =========================================================
-- CONTROLE DE ENTREGA SPED
-- =========================================================

CREATE TABLE sped_deliveries (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    company_id UUID NOT NULL REFERENCES companies(id),

    sped_type VARCHAR(50),
    -- ECD
    -- ECF
    -- EFD
    -- REINF

    fiscal_year INT,

    protocol VARCHAR(255),

    receipt_number VARCHAR(255),

    delivered_at TIMESTAMP,

    status VARCHAR(50)
);



-- =========================================================
-- FILAS DE PROCESSAMENTO
-- =========================================================

CREATE TABLE background_jobs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    queue_name VARCHAR(100),

    payload JSONB,

    status VARCHAR(50) DEFAULT 'PENDING',

    retries INT DEFAULT 0,

    created_at TIMESTAMP DEFAULT NOW(),

    processed_at TIMESTAMP
);



-- =========================================================
-- CONFIGURAÇÕES POR EMPRESA
-- =========================================================

CREATE TABLE company_settings (
    company_id UUID PRIMARY KEY
        REFERENCES companies(id),

    allow_negative_cash BOOLEAN DEFAULT FALSE,

    auto_close_period BOOLEAN DEFAULT FALSE,

    default_report_template UUID
        REFERENCES report_templates(id),

    created_at TIMESTAMP DEFAULT NOW()
);



-- =========================================================
-- VIEW DE PERMISSÕES EFETIVAS
-- =========================================================

CREATE VIEW user_permissions_view AS
SELECT
    uc.user_id,
    uc.company_id,
    p.code AS permission_code

FROM user_companies uc

JOIN role_permissions rp
    ON rp.role_id = uc.role_id

JOIN permissions p
    ON p.id = rp.permission_id;



-- =========================================================
-- FUNÇÃO DE LOGIN
-- EXEMPLO
-- =========================================================

/*

SELECT *
FROM users
WHERE email = :email
AND password_hash = crypt(:password, password_hash);

*/



-- =========================================================
-- FUNÇÃO DE PERMISSÃO
-- =========================================================

/*

SELECT EXISTS (
    SELECT 1
    FROM user_permissions_view
    WHERE user_id = :user_id
    AND company_id = :company_id
    AND permission_code = 'ENTRY_CREATE'
);

*/



-- =========================================================
-- ESTRUTURA FINAL
-- =========================================================

/*

COM ISSO VOCÊ TEM:

✔ ERP CONTÁBIL MULTIEMPRESA
✔ MULTIUSUÁRIO
✔ RBAC (ROLE BASED ACCESS CONTROL)
✔ PLANO DE CONTAS FLEXÍVEL
✔ RELATÓRIOS CUSTOMIZÁVEIS
✔ VERSIONAMENTO
✔ TRAVA CONTÁBIL
✔ SPED
✔ ECD
✔ ASSINATURA DIGITAL
✔ AUDITORIA
✔ LOGS
✔ BASE PARA SAAS

Essa arquitetura já começa a entrar
no nível de sistemas como:

- Domínio
- Alterdata
- SCI
- Questor
- Omie Contábil
- Conta Azul (backoffice)
- Netsuite
- SAP FI

*/


