PRAGMA foreign_keys=OFF;

CREATE TABLE lancamento_new (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  empresa_id INTEGER,
  data TEXT NOT NULL,
  numero TEXT,
  historico TEXT,
  tipo TEXT DEFAULT 'N',
  created_at TEXT DEFAULT CURRENT_TIMESTAMP,

  FOREIGN KEY (empresa_id) REFERENCES empresa(id)
);

INSERT INTO lancamento_new (
  id,
  empresa_id,
  data,
  numero,
  historico,
  tipo,
  created_at
)
SELECT
  id,
  empresa_id,
  data,
  numero,
  historico,
  tipo,
  created_at
FROM lancamento;

DROP TABLE lancamento;

ALTER TABLE lancamento_new
RENAME TO lancamento;

CREATE INDEX idx_lancamento_data
ON lancamento(data);

PRAGMA foreign_keys=ON;
