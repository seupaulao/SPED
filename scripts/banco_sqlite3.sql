PRAGMA foreign_keys = ON;

create table tomador (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  cnpj TEXT NOT NULL,
  nome TEXT NOT NULL,
  uf TEXT,
  municipio TEXT,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP,
  excluido_at TEXT
);

create table nota_fiscal (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  numero INTEGER,
  codigo TEXT,
  chave_acesso TEXT,
  situacao TEXT,
  data_emissao TEXT,
  valor_total REAL,
  empresa_id INTEGER,
  tomador_id INTEGER,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP,
  excluido_at TEXT
);

CREATE TABLE empresa (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  cnpj TEXT NOT NULL,
  nome TEXT NOT NULL,
  uf TEXT,
  municipio TEXT,
  data_inicio TEXT,
  data_fim TEXT,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP,
  excluido_at TEXT,
  viabilidade TEXT
);

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
  created_at TEXT DEFAULT CURRENT_TIMESTAMP,
  excluido_at TEXT,

  FOREIGN KEY (empresa_id) REFERENCES empresa(id),
  FOREIGN KEY (conta_pai_id) REFERENCES plano_contas(id)
);

CREATE TABLE lancamento (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  empresa_id INTEGER,
  data TEXT NOT NULL,
  numero TEXT,                 -- esse campo pode estar denro do campo abaixo
  historico TEXT,              -- numero e historico são um só campo 
  tipo TEXT DEFAULT 'N',       -- N - Normal, E - Estorno, A - Ajuste
  created_at TEXT DEFAULT CURRENT_TIMESTAMP,
  excluido_at TEXT,

  FOREIGN KEY (empresa_id) REFERENCES empresa(id)
);

CREATE TABLE lancamento_item (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  lancamento_id INTEGER,
  conta_id INTEGER,
  tipo TEXT NOT NULL, -- D ou C
  valor REAL NOT NULL,
  excluido_at TEXT,

  FOREIGN KEY (lancamento_id) REFERENCES lancamento(id) ON DELETE CASCADE,
  FOREIGN KEY (conta_id) REFERENCES plano_contas(id)
);

CREATE TABLE mapa_demonstracoes (
  id INTEGER PRIMARY KEY AUTOINCREMENT ,
  conta_id INTEGER,
  tipo TEXT, -- DRE, DVA, DFC
  categoria TEXT,
  excluido_at TEXT,

  FOREIGN KEY (conta_id) REFERENCES plano_contas(id)
);

CREATE INDEX idx_lancamento_data ON lancamento(data);
CREATE INDEX idx_lancamento_item_conta ON lancamento_item(conta_id);

CREATE TABLE trava_contabil (
    id TEXT PRIMARY KEY,
    empresa_id TEXT NOT NULL REFERENCES empresas(id),
    year INTEGER NOT NULL,
    month INTEGER NOT NULL,
    is_closed INTEGER DEFAULT 0,
    closed_by TEXT REFERENCES usuarios(id),
    closed_at TEXT
);

-- CREATE TABLE sped_mappings (
--     id TEXT PRIMARY KEY,
--     conta_id TEXT NOT NULL REFERENCES plano_contas(id),
--     sped_code TEXT NOT NULL,
--     description TEXT
-- );

-- CREATE TABLE usuarios (
--     id TEXT PRIMARY KEY,
--     nome TEXT NOT NULL,
--     email TEXT UNIQUE NOT NULL,
--     password_hash TEXT NOT NULL,
--     is_active INTEGER DEFAULT 1,
--     last_login_at TEXT,
--     created_at TEXT DEFAULT (datetime('now'))
-- );

-- CREATE TABLE audit_logs (
--     id TEXT PRIMARY KEY,
--     company_id TEXT REFERENCES empresas(id),
--     user_id TEXT REFERENCES usuarios(id),
--     entity_name TEXT,
--     entity_id TEXT,
--     action TEXT,
--     old_data TEXT,
--     new_data TEXT,
--     created_at TEXT DEFAULT (datetime('now'))
-- );

-- CREATE TABLE certificados_digitais (
--     id TEXT PRIMARY KEY,
--     empresa_id TEXT NOT NULL REFERENCES empresas(id),
--     certificate_name TEXT,
--     serial_number TEXT,
--     valid_from TEXT,
--     valid_until TEXT,
--     issuer TEXT,
--     encrypted_pfx BLOB,
--     created_at TEXT DEFAULT (datetime('now'))
-- );

-- CREATE TABLE ecd_arquivos (
--     id TEXT PRIMARY KEY,
--     empresa_id TEXT NOT NULL REFERENCES empresas(id),
--     fiscal_year INTEGER NOT NULL,
--     file_name TEXT,
--     file_hash TEXT,
--     generated_by TEXT REFERENCES usuarios(id),
--     generated_at TEXT DEFAULT (datetime('now')),
--     signed_at TEXT,
--     delivered_at TEXT,
--     status TEXT
-- );

-- CREATE TABLE assinaturas_digitais (
--     id TEXT PRIMARY KEY,
--     ecd_arquivo_id TEXT NOT NULL REFERENCES ecd_arquivos(id),
--     signed_by TEXT REFERENCES usuarios(id),
--     certificate_id TEXT REFERENCES digital_certificates(id),
--     signature_hash TEXT NOT NULL,
--     signed_at TEXT DEFAULT (datetime('now'))
-- );

-- CREATE TABLE sped_entregas (
--     id TEXT PRIMARY KEY,
--     empresa_id TEXT NOT NULL REFERENCES empresas(id),
--     sped_type TEXT,
--     fiscal_year INTEGER,
--     protocol TEXT,
--     receipt_number TEXT,
--     delivered_at TEXT,
--     status TEXT
-- );

-- CREATE TABLE jobs (
--     id TEXT PRIMARY KEY,
--     queue_name TEXT,
--     payload TEXT,
--     status TEXT DEFAULT 'PENDING',
--     retries INTEGER DEFAULT 0,
--     created_at TEXT DEFAULT (datetime('now')),
--     processed_at TEXT
-- );