PRAGMA foreign_keys = ON;

CREATE TABLE empresa (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  cnpj TEXT NOT NULL,
  nome TEXT NOT NULL,
  uf TEXT,
  municipio TEXT,
  data_inicio TEXT,
  data_fim TEXT,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP
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

  FOREIGN KEY (empresa_id) REFERENCES empresa(id),
  FOREIGN KEY (conta_pai_id) REFERENCES plano_contas(id)
);

CREATE TABLE historico_padrao (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  empresa_id INTEGER,
  codigo TEXT,
  descricao TEXT NOT NULL,

  FOREIGN KEY (empresa_id) REFERENCES empresa(id)
);

CREATE TABLE lancamento (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  empresa_id INTEGER,
  data TEXT NOT NULL,
  numero TEXT,
  historico TEXT,
  historico_padrao_id INTEGER,
  valor_total REAL,
  tipo TEXT DEFAULT 'N',
  created_at TEXT DEFAULT CURRENT_TIMESTAMP,

  FOREIGN KEY (empresa_id) REFERENCES empresa(id),
  FOREIGN KEY (historico_padrao_id) REFERENCES historico_padrao(id)
);

CREATE TABLE lancamento_item (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  lancamento_id INTEGER,
  conta_id INTEGER,
  tipo TEXT NOT NULL, -- D ou C
  valor REAL NOT NULL,
  historico TEXT,

  FOREIGN KEY (lancamento_id) REFERENCES lancamento(id) ON DELETE CASCADE,
  FOREIGN KEY (conta_id) REFERENCES plano_contas(id)
);

CREATE TABLE mapa_demonstracoes (
  id INTEGER PRIMARY KEY AUTOINCREMENT ,
  conta_id INTEGER,
  tipo TEXT, -- DRE, DVA, DFC
  categoria TEXT,

  FOREIGN KEY (conta_id) REFERENCES plano_contas(id)
);

CREATE INDEX idx_lancamento_data ON lancamento(data);
CREATE INDEX idx_lancamento_item_conta ON lancamento_item(conta_id);
