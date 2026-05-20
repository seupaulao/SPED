PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE empresa (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  cnpj TEXT NOT NULL,
  nome TEXT NOT NULL,
  uf TEXT,
  municipio TEXT,
  data_inicio TEXT,
  data_fim TEXT,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP
, excluido_em TEXT);
INSERT INTO empresa VALUES(1,'06211011000111','PAOLA LTDA','CE','Fortaleza','2026-05-14',NULL,'2026-05-15 16:47:09',NULL);
INSERT INTO empresa VALUES(2,'2842883288383','alguma outra','ce','fortaleza','2026-05-18',NULL,'2026-05-17 21:42:15',NULL);
CREATE TABLE plano_contas (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  empresa_id INTEGER,
  codigo TEXT NOT NULL,
  descricao TEXT NOT NULL,
  tipo TEXT NOT NULL, -- S ou A
  natureza TEXT, -- D ou C
  grupo TEXT,
  dre_grupo TEXT,
  subgrupo TEXT,
  fluxo_caixa_tipo TEXT,
  nivel INTEGER NOT NULL,
  conta_pai_id INTEGER,
  codigo_referencial TEXT,
  aceita_lancamento INTEGER DEFAULT 1,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP, excluido_em TEXT,

  FOREIGN KEY (empresa_id) REFERENCES empresa(id),
  FOREIGN KEY (conta_pai_id) REFERENCES plano_contas(id)
);
INSERT INTO plano_contas VALUES(1,1,'1','ativo','S','D','ATIVO',NULL,NULL,NULL,1,NULL,NULL,0,'2026-05-15 16:43:54',NULL);
INSERT INTO plano_contas VALUES(2,1,'2','passivo','S','C','PASSIVO',NULL,NULL,NULL,1,NULL,NULL,0,'2026-05-15 16:43:54',NULL);
INSERT INTO plano_contas VALUES(3,1,'3','patrimonioliquido','S','C','PL',NULL,NULL,NULL,1,NULL,NULL,0,'2026-05-15 16:43:54',NULL);
INSERT INTO plano_contas VALUES(4,1,'4','receita','S','C',NULL,'RECEITA_BRUTA',NULL,NULL,1,NULL,NULL,0,'2026-05-15 16:43:54',NULL);
INSERT INTO plano_contas VALUES(5,1,'5','despesa','S','D',NULL,NULL,NULL,NULL,1,NULL,NULL,0,'2026-05-15 16:43:54',NULL);
INSERT INTO plano_contas VALUES(6,1,'1.1','ativo:caixa','A','D','ATIVO',NULL,NULL,NULL,2,1,NULL,1,'2026-05-15 16:43:54',NULL);
INSERT INTO plano_contas VALUES(7,1,'1.2','ativo:banco','S','D','ATIVO',NULL,NULL,NULL,2,1,NULL,0,'2026-05-15 16:43:54',NULL);
INSERT INTO plano_contas VALUES(8,1,'1.2.1','ativo:banco:conta_corrente','A','D','ATIVO',NULL,NULL,NULL,3,7,NULL,1,'2026-05-15 16:43:54',NULL);
INSERT INTO plano_contas VALUES(9,1,'1.2.2','ativo:banco:conta_digital','A','D','ATIVO',NULL,NULL,NULL,3,7,NULL,1,'2026-05-15 16:43:54',NULL);
INSERT INTO plano_contas VALUES(10,1,'1.3','ativo:contas_a_receber','S','D','ATIVO',NULL,NULL,NULL,2,1,NULL,0,'2026-05-15 16:43:54',NULL);
INSERT INTO plano_contas VALUES(11,1,'1.3.1','ativo:contas_a_receber:hospital_a','A','D','ATIVO',NULL,NULL,NULL,3,10,NULL,1,'2026-05-15 16:43:54',NULL);
INSERT INTO plano_contas VALUES(12,1,'1.3.2','ativo:contas_a_receber:hospital_b','A','D','ATIVO',NULL,NULL,NULL,3,10,NULL,1,'2026-05-15 16:43:54',NULL);
INSERT INTO plano_contas VALUES(13,1,'1.4','ativo:imobilizado','S','D','ATIVO',NULL,NULL,NULL,2,1,NULL,0,'2026-05-15 16:43:54',NULL);
INSERT INTO plano_contas VALUES(14,1,'1.4.1','ativo:imobilizado:equipamentos','A','D','ATIVO',NULL,NULL,NULL,3,13,NULL,1,'2026-05-15 16:43:54',NULL);
INSERT INTO plano_contas VALUES(15,1,'1.4.2','ativo:imobilizado:computadores','A','D','ATIVO',NULL,NULL,NULL,3,13,NULL,1,'2026-05-15 16:43:54',NULL);
INSERT INTO plano_contas VALUES(16,1,'2.1','passivo:fornecedores','A','C','PASSIVO',NULL,NULL,NULL,2,2,NULL,1,'2026-05-15 16:43:54',NULL);
INSERT INTO plano_contas VALUES(17,1,'2.2','passivo:impostos','S','C','PASSIVO',NULL,NULL,NULL,2,2,NULL,0,'2026-05-15 16:43:54',NULL);
INSERT INTO plano_contas VALUES(18,1,'2.2.1','passivo:impostos:das','A','C','PASSIVO',NULL,NULL,NULL,3,17,NULL,1,'2026-05-15 16:43:54',NULL);
INSERT INTO plano_contas VALUES(19,1,'2.2.2','passivo:impostos:iss','A','C','PASSIVO',NULL,NULL,NULL,3,17,NULL,1,'2026-05-15 16:43:54',NULL);
INSERT INTO plano_contas VALUES(20,1,'2.3','passivo:inss','A','C','PASSIVO',NULL,NULL,NULL,2,2,NULL,1,'2026-05-15 16:43:54',NULL);
INSERT INTO plano_contas VALUES(21,1,'2.4','passivo:prolabore','A','C','PASSIVO',NULL,NULL,NULL,2,2,NULL,1,'2026-05-15 16:43:54',NULL);
INSERT INTO plano_contas VALUES(22,1,'3.1','patrimonioliquido:capital_social','A','C','PL',NULL,NULL,NULL,2,3,NULL,1,'2026-05-15 16:43:54',NULL);
INSERT INTO plano_contas VALUES(23,1,'3.2','patrimonioliquido:lucros_acumulados','A','C','PL',NULL,NULL,NULL,2,3,NULL,1,'2026-05-15 16:43:54',NULL);
INSERT INTO plano_contas VALUES(24,1,'3.3','patrimonioliquido:distribuicao_lucros','A','C','PL',NULL,NULL,NULL,2,3,NULL,1,'2026-05-15 16:43:54',NULL);
INSERT INTO plano_contas VALUES(25,1,'4.1','receita:plantao','S','C',NULL,'RECEITA_BRUTA',NULL,NULL,2,4,NULL,0,'2026-05-15 16:43:54',NULL);
INSERT INTO plano_contas VALUES(26,1,'4.1.1','receita:plantao:hospital_a','A','C',NULL,'RECEITA_BRUTA','RECEITAS',NULL,3,25,NULL,1,'2026-05-15 16:43:54',NULL);
INSERT INTO plano_contas VALUES(27,1,'4.1.2','receita:plantao:hospital_b','A','C',NULL,'RECEITA_BRUTA','RECEITAS',NULL,3,25,NULL,1,'2026-05-15 16:43:54',NULL);
INSERT INTO plano_contas VALUES(28,1,'4.2','receita:consultas','A','C',NULL,'RECEITA_BRUTA','RECEITAS',NULL,2,4,NULL,1,'2026-05-15 16:43:54',NULL);
INSERT INTO plano_contas VALUES(29,1,'4.3','receita:rendimentos','A','C',NULL,'RECEITA_BRUTA','RECEITAS',NULL,2,4,NULL,1,'2026-05-15 16:43:54',NULL);
INSERT INTO plano_contas VALUES(30,1,'5.1','despesa:aluguel','A','D',NULL,'DESPESA_OPERACIONAL','CAPITAL_TERCEIROS',NULL,2,5,NULL,1,'2026-05-15 16:43:54',NULL);
INSERT INTO plano_contas VALUES(31,1,'5.2','despesa:internet','A','D',NULL,'DESPESA_OPERACIONAL','CAPITAL_TERCEIROS',NULL,2,5,NULL,1,'2026-05-15 16:43:54',NULL);
INSERT INTO plano_contas VALUES(32,1,'5.3','despesa:energia','A','D',NULL,'DESPESA_OPERACIONAL','INSUMOS',NULL,2,5,NULL,1,'2026-05-15 16:43:54',NULL);
INSERT INTO plano_contas VALUES(33,1,'5.4','despesa:software','A','D',NULL,'DESPESA_OPERACIONAL','CAPITAL_TERCEIROS',NULL,2,5,NULL,1,'2026-05-15 16:43:54',NULL);
INSERT INTO plano_contas VALUES(34,1,'5.5','despesa:contabilidade','A','D',NULL,'DESPESA_OPERACIONAL','CAPITAL_TERCEIROS',NULL,2,5,NULL,1,'2026-05-15 16:43:54',NULL);
INSERT INTO plano_contas VALUES(35,1,'5.6','despesa:prolabore','A','D',NULL,'DESPESA_OPERACIONAL','PESSOAL',NULL,2,5,NULL,1,'2026-05-15 16:43:54',NULL);
INSERT INTO plano_contas VALUES(36,1,'5.7','despesa:inss','A','D',NULL,'DESPESA_OPERACIONAL','PESSOAL',NULL,2,5,NULL,1,'2026-05-15 16:43:54',NULL);
INSERT INTO plano_contas VALUES(37,1,'5.8','despesa:das','A','D',NULL,'DESPESA_OPERACIONAL','IMPOSTOS',NULL,2,5,NULL,1,'2026-05-15 16:43:54',NULL);
INSERT INTO plano_contas VALUES(38,1,'5.9','despesa:iss','A','D',NULL,'DESPESA_OPERACIONAL','IMPOSTOS',NULL,2,5,NULL,1,'2026-05-15 16:43:54',NULL);
INSERT INTO plano_contas VALUES(39,1,'5.10','despesa:tarifas','A','D',NULL,'RESULTADO_FINANCEIRO','CAPITAL_TERCEIROS',NULL,2,5,NULL,1,'2026-05-15 16:43:54',NULL);
INSERT INTO plano_contas VALUES(40,1,'5.11','despesa:juros','A','D',NULL,'RESULTADO_FINANCEIRO','CAPITAL_TERCEIROS',NULL,2,5,NULL,1,'2026-05-15 16:43:54',NULL);
CREATE TABLE lancamento (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  empresa_id INTEGER,
  data TEXT NOT NULL,
  numero TEXT,                 -- esse campo pode estar denro do campo abaixo
  historico TEXT,              -- numero e historico são um só campo 
  tipo TEXT DEFAULT 'N',       -- N - Normal, E - Estorno, A - Ajuste
  created_at TEXT DEFAULT CURRENT_TIMESTAMP, excluido_em TEXT,

  FOREIGN KEY (empresa_id) REFERENCES empresa(id)
);
INSERT INTO lancamento VALUES(1,1,'2026-05-19',NULL,'alguma coisa','N','2026-05-19 16:03:17',NULL);
CREATE TABLE lancamento_item (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  lancamento_id INTEGER,
  conta_id INTEGER,
  tipo TEXT NOT NULL, -- D ou C
  valor REAL NOT NULL, excluido_em TEXT,

  FOREIGN KEY (lancamento_id) REFERENCES lancamento(id) ON DELETE CASCADE,
  FOREIGN KEY (conta_id) REFERENCES plano_contas(id)
);
INSERT INTO lancamento_item VALUES(1,1,8,'D',3000.0,NULL);
INSERT INTO lancamento_item VALUES(2,1,29,'C',3000.0,NULL);
CREATE TABLE mapa_demonstracoes (
  id INTEGER PRIMARY KEY AUTOINCREMENT ,
  conta_id INTEGER,
  tipo TEXT, -- DRE, DVA, DFC
  categoria TEXT,

  FOREIGN KEY (conta_id) REFERENCES plano_contas(id)
);
CREATE TABLE report_types (
    id TEXT PRIMARY KEY,
    code TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL
);
INSERT INTO report_types VALUES('4ba4448ae0c0739f57f901cb9ce4e28b','BALANCO','Balanço Patrimonial');
INSERT INTO report_types VALUES('a0b2b220151acf28a4cb6efc6e612fb0','DRE','Demonstração do Resultado');
INSERT INTO report_types VALUES('a2a97dc9ddeb09f2e9a7f43c76a1a99f','DFC','Demonstração do Fluxo de Caixa');
INSERT INTO report_types VALUES('0bcc1c1ae84165dcfba15d1334d0f698','DVA','Demonstração do Valor Adicionado');
INSERT INTO report_types VALUES('fce957ddccf07cb5dd71c0c2a663ea63','BALANCETE','Balancete');
CREATE TABLE plano_contas_referencial (
    id TEXT PRIMARY KEY,

    parent_id TEXT REFERENCES plano_contas_referencial(id),

    codigo TEXT NOT NULL,
    nome TEXT NOT NULL,

    tipo_conta TEXT NOT NULL,
    level INTEGER NOT NULL DEFAULT 1,
    aceita_entrada INTEGER DEFAULT 0,
    is_ativo INTEGER DEFAULT 1,
    tipo TEXT,
    natureza TEXT,
    nivel INTEGER,
    grupo TEXT,
    dre_grupo TEXT,
    fluxo_caixa_tipo TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    excluded_at TEXT
);
CREATE TABLE centro_custo (
    id TEXT PRIMARY KEY,
    empresa_id TEXT NOT NULL REFERENCES empresa(id),
    codigo TEXT,
    nome TEXT NOT NULL,
    created_at TEXT DEFAULT (datetime('now'))
);
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
CREATE TABLE tags (
    id TEXT PRIMARY KEY,
    company_id TEXT REFERENCES companies(id),
    name TEXT NOT NULL
);
CREATE TABLE journal_entry_line_tags (
    line_id TEXT REFERENCES journal_entry_lines(id),
    tag_id TEXT REFERENCES tags(id),
    PRIMARY KEY (line_id, tag_id)
);
CREATE TABLE sped_mappings (
    id TEXT PRIMARY KEY,
    conta_id TEXT NOT NULL REFERENCES plano_contas(id),
    sped_code TEXT NOT NULL,
    description TEXT
);
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
INSERT INTO regras VALUES('e61bfc126115b1c40592f72d1ed179ef','SUPER_ADMIN','Super Administrador');
INSERT INTO regras VALUES('1f45652cda4b95c0cf9a227492aaf735','ACCOUNTANT','Contador');
INSERT INTO regras VALUES('e5087a4c741fad9a8204bd4c27114524','ASSISTANT','Assistente Contábil');
INSERT INTO regras VALUES('55a805c9e909b2a35781fb25a407e3b9','AUDITOR','Auditor');
INSERT INTO regras VALUES('3257c755155a818f9405865671523bc5','CLIENT','Cliente');
CREATE TABLE permissoes (
    id TEXT PRIMARY KEY,
    code TEXT UNIQUE NOT NULL,
    descricao TEXT
);
INSERT INTO permissoes VALUES('3134af556de9f4798d9771f9dbdcea0d','COMPANY_VIEW','Visualizar empresas');
INSERT INTO permissoes VALUES('d7e9089e92b381232f3a6586ed415187','COMPANY_EDIT','Editar empresas');
INSERT INTO permissoes VALUES('e5e2bcae7c5d9a253c6c5f27a8183375','ACCOUNT_VIEW','Visualizar plano de contas');
INSERT INTO permissoes VALUES('1fea85203aaf05435d234a61263b86f7','ACCOUNT_EDIT','Editar plano de contas');
INSERT INTO permissoes VALUES('a784c7e81304cb28c793641753a38248','ENTRY_VIEW','Visualizar lançamentos');
INSERT INTO permissoes VALUES('54bc1ebf30421c4ecb1db9b57132358b','ENTRY_CREATE','Criar lançamentos');
INSERT INTO permissoes VALUES('00bc2c6b6f023ce59acfac638026daea','ENTRY_EDIT','Editar lançamentos');
INSERT INTO permissoes VALUES('b236ce6c514dbf6c114fd3a855ba9455','REPORT_VIEW','Visualizar relatórios');
INSERT INTO permissoes VALUES('989fb6ff2ba12e949b92fe2f559a0e87','REPORT_EDIT','Editar relatórios');
INSERT INTO permissoes VALUES('4286cd0e46d541331f5c74482a4b15d6','SPED_EXPORT','Exportar SPED');
INSERT INTO permissoes VALUES('4a9b3a4c9882bb96f6c7d3b330dbbdcc','ECD_SIGN','Assinar ECD');
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
INSERT INTO sped_natureza VALUES('b0f9d18cad046481f904147472bc12cf','01','Contas de Ativo');
INSERT INTO sped_natureza VALUES('b6dc5d9e892bd44eb22b47edb66697d6','02','Contas de Passivo');
INSERT INTO sped_natureza VALUES('19f89a94e009390272bb852854638378','03','Patrimônio Líquido');
INSERT INTO sped_natureza VALUES('f71c8713afb40d53f5cde056a3ac37ef','04','Receitas');
INSERT INTO sped_natureza VALUES('cd3633b4ea01a23d9e794966ebde0407','05','Custos');
INSERT INTO sped_natureza VALUES('17548147635eedb6ec7969515d48d7bb','06','Despesas');
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
CREATE TABLE empresa_configuracao (
    empresa_id TEXT PRIMARY KEY REFERENCES companies(id),
    permitir_dinheiro_negativo INTEGER DEFAULT 0,
    periodo_fechamento_automatico INTEGER DEFAULT 0,
    default_report_template TEXT REFERENCES report_templates(id),
    created_at TEXT DEFAULT (datetime('now'))
);
DELETE FROM sqlite_sequence;
INSERT INTO sqlite_sequence VALUES('plano_contas',40);
INSERT INTO sqlite_sequence VALUES('empresa',2);
INSERT INTO sqlite_sequence VALUES('lancamento',1);
INSERT INTO sqlite_sequence VALUES('lancamento_item',2);
CREATE INDEX idx_lancamento_data ON lancamento(data);
CREATE INDEX idx_lancamento_item_conta ON lancamento_item(conta_id);
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
COMMIT;
