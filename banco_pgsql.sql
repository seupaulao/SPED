CREATE TABLE empresa (
  id SERIAL PRIMARY KEY,
  cnpj VARCHAR(14) NOT NULL,
  nome TEXT NOT NULL,
  uf CHAR(2),
  municipio TEXT,
  data_inicio DATE,
  data_fim DATE,
  created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE plano_contas (
  id SERIAL PRIMARY KEY,
  empresa_id INT REFERENCES empresa(id),
  codigo VARCHAR(20) NOT NULL,
  descricao TEXT NOT NULL,
  tipo CHAR(1) NOT NULL, -- S=Sintética, A=Analítica
  natureza CHAR(1), -- D ou C
  nivel INT NOT NULL,
  conta_pai_id INT REFERENCES plano_contas(id),
  codigo_referencial VARCHAR(20),
  aceita_lancamento BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE historico_padrao (
  id SERIAL PRIMARY KEY,
  empresa_id INT REFERENCES empresa(id),
  codigo VARCHAR(10),
  descricao TEXT NOT NULL
);

CREATE TABLE lancamento (
  id SERIAL PRIMARY KEY,
  empresa_id INT REFERENCES empresa(id),
  data DATE NOT NULL,
  numero VARCHAR(20),
  historico TEXT,
  historico_padrao_id INT REFERENCES historico_padrao(id),
  valor_total NUMERIC(14,2),
  tipo CHAR(1) DEFAULT 'N', -- N=Normal, E=Encerramento
  created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE lancamento_item (
  id SERIAL PRIMARY KEY,
  lancamento_id INT REFERENCES lancamento(id) ON DELETE CASCADE,
  conta_id INT REFERENCES plano_contas(id),
  tipo CHAR(1) NOT NULL, -- D ou C
  valor NUMERIC(14,2) NOT NULL,
  historico TEXT
);

--evolucao para conta resultado

ALTER TABLE plano_contas ADD COLUMN grupo TEXT;
-- Ex:
-- ATIVO, PASSIVO, PL, RECEITA, DESPESA

ALTER TABLE plano_contas ADD COLUMN subgrupo TEXT;
-- Ex:
-- CIRCULANTE, NAO_CIRCULANTE, OPERACIONAL, FINANCEIRO

ALTER TABLE plano_contas ADD COLUMN dre_grupo TEXT;
-- Ex:
-- RECEITA_BRUTA, CUSTO, DESPESA_OPERACIONAL, RESULTADO_FINANCEIRO

ALTER TABLE plano_contas ADD COLUMN fluxo_caixa_tipo TEXT;
-- Ex:
-- OPERACIONAL, INVESTIMENTO, FINANCIAMENTO

CREATE TABLE mapa_demonstracoes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  conta_id INTEGER,
  tipo TEXT, -- DRE, DVA, DFC
  categoria TEXT,

  FOREIGN KEY (conta_id) REFERENCES plano_contas(id)
);


