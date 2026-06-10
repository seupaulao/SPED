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
  created_at TEXT DEFAULT CURRENT_TIMESTAMP,
  excluido_at TEXT
, viabilidade text);
INSERT INTO empresa VALUES(1,'19394023000156','TECH INFO TESTE','CE','FORTALEZA','2026-05-14',NULL,'2026-05-25 22:03:06',NULL,NULL);
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
INSERT INTO plano_contas VALUES(1,1,'1','ativo','S','D','ATIVO',NULL,NULL,NULL,1,NULL,NULL,0,'2026-05-25 22:01:03',NULL);
INSERT INTO plano_contas VALUES(2,1,'2','passivo','S','C','PASSIVO',NULL,NULL,NULL,1,NULL,NULL,0,'2026-05-25 22:01:03',NULL);
INSERT INTO plano_contas VALUES(3,1,'3','patrimonioliquido','S','C','PL',NULL,NULL,NULL,1,NULL,NULL,0,'2026-05-25 22:01:03',NULL);
INSERT INTO plano_contas VALUES(4,1,'4','receita','S','C',NULL,'RECEITA_BRUTA',NULL,NULL,1,NULL,NULL,0,'2026-05-25 22:01:03',NULL);
INSERT INTO plano_contas VALUES(5,1,'5','despesa','S','D',NULL,NULL,NULL,NULL,1,NULL,NULL,0,'2026-05-25 22:01:03',NULL);
INSERT INTO plano_contas VALUES(6,1,'1.1','ativo:caixa','A','D','ATIVO',NULL,NULL,NULL,2,1,NULL,1,'2026-05-25 22:01:04',NULL);
INSERT INTO plano_contas VALUES(7,1,'1.2','ativo:banco','S','D','ATIVO',NULL,NULL,NULL,2,1,NULL,0,'2026-05-25 22:01:04',NULL);
INSERT INTO plano_contas VALUES(8,1,'1.2.1','ativo:banco:conta_corrente','A','D','ATIVO',NULL,NULL,NULL,3,7,NULL,1,'2026-05-25 22:01:04',NULL);
INSERT INTO plano_contas VALUES(9,1,'1.2.2','ativo:banco:conta_digital','A','D','ATIVO',NULL,NULL,NULL,3,7,NULL,1,'2026-05-25 22:01:04',NULL);
INSERT INTO plano_contas VALUES(10,1,'1.3','ativo:contas_a_receber','S','D','ATIVO',NULL,NULL,NULL,2,1,NULL,0,'2026-05-25 22:01:04',NULL);
INSERT INTO plano_contas VALUES(11,1,'1.3.1','ativo:contas_a_receber:hospital_a','A','D','ATIVO',NULL,NULL,NULL,3,10,NULL,1,'2026-05-25 22:01:04',NULL);
INSERT INTO plano_contas VALUES(12,1,'1.3.2','ativo:contas_a_receber:hospital_b','A','D','ATIVO',NULL,NULL,NULL,3,10,NULL,1,'2026-05-25 22:01:04',NULL);
INSERT INTO plano_contas VALUES(13,1,'1.4','ativo:imobilizado','S','D','ATIVO',NULL,NULL,NULL,2,1,NULL,0,'2026-05-25 22:01:04',NULL);
INSERT INTO plano_contas VALUES(14,1,'1.4.1','ativo:imobilizado:equipamentos','A','D','ATIVO',NULL,NULL,NULL,3,13,NULL,1,'2026-05-25 22:01:04',NULL);
INSERT INTO plano_contas VALUES(15,1,'1.4.2','ativo:imobilizado:computadores','A','D','ATIVO',NULL,NULL,NULL,3,13,NULL,1,'2026-05-25 22:01:04',NULL);
INSERT INTO plano_contas VALUES(16,1,'2.1','passivo:fornecedores','A','C','PASSIVO',NULL,NULL,NULL,2,2,NULL,1,'2026-05-25 22:01:04',NULL);
INSERT INTO plano_contas VALUES(17,1,'2.2','passivo:impostos','S','C','PASSIVO',NULL,NULL,NULL,2,2,NULL,0,'2026-05-25 22:01:04',NULL);
INSERT INTO plano_contas VALUES(18,1,'2.2.1','passivo:impostos:das','A','C','PASSIVO',NULL,NULL,NULL,3,17,NULL,1,'2026-05-25 22:01:04',NULL);
INSERT INTO plano_contas VALUES(19,1,'2.2.2','passivo:impostos:iss','A','C','PASSIVO',NULL,NULL,NULL,3,17,NULL,1,'2026-05-25 22:01:04',NULL);
INSERT INTO plano_contas VALUES(20,1,'2.3','passivo:inss','A','C','PASSIVO',NULL,NULL,NULL,2,2,NULL,1,'2026-05-25 22:01:04',NULL);
INSERT INTO plano_contas VALUES(21,1,'2.4','passivo:prolabore','A','C','PASSIVO',NULL,NULL,NULL,2,2,NULL,1,'2026-05-25 22:01:04',NULL);
INSERT INTO plano_contas VALUES(22,1,'3.1','patrimonioliquido:capital_social','A','C','PL',NULL,NULL,NULL,2,3,NULL,1,'2026-05-25 22:01:04',NULL);
INSERT INTO plano_contas VALUES(23,1,'3.2','patrimonioliquido:lucros_acumulados','A','C','PL',NULL,NULL,NULL,2,3,NULL,1,'2026-05-25 22:01:04',NULL);
INSERT INTO plano_contas VALUES(24,1,'3.3','patrimonioliquido:distribuicao_lucros','A','C','PL',NULL,NULL,NULL,2,3,NULL,1,'2026-05-25 22:01:04',NULL);
INSERT INTO plano_contas VALUES(25,1,'4.1','receita:servico','S','C',NULL,'RECEITA_BRUTA',NULL,NULL,2,4,NULL,0,'2026-05-25 22:01:04',NULL);
INSERT INTO plano_contas VALUES(26,1,'4.1.1','receita:servico:fornecedor_a','A','C',NULL,'RECEITA_BRUTA','RECEITAS',NULL,3,25,NULL,1,'2026-05-25 22:01:04',NULL);
INSERT INTO plano_contas VALUES(27,1,'4.1.2','receita:servico:fornecedor_b','A','C',NULL,'RECEITA_BRUTA','RECEITAS',NULL,3,25,NULL,1,'2026-05-25 22:01:04',NULL);
INSERT INTO plano_contas VALUES(28,1,'4.2','receita:consultas','A','C',NULL,'RECEITA_BRUTA','RECEITAS',NULL,2,4,NULL,1,'2026-05-25 22:01:04',NULL);
INSERT INTO plano_contas VALUES(29,1,'4.3','receita:rendimentos','A','C',NULL,'RECEITA_BRUTA','RECEITAS',NULL,2,4,NULL,1,'2026-05-25 22:01:04',NULL);
INSERT INTO plano_contas VALUES(30,1,'5.1','despesa:aluguel','A','D',NULL,'DESPESA_OPERACIONAL','CAPITAL_TERCEIROS',NULL,2,5,NULL,1,'2026-05-25 22:01:04',NULL);
INSERT INTO plano_contas VALUES(31,1,'5.2','despesa:internet','A','D',NULL,'DESPESA_OPERACIONAL','CAPITAL_TERCEIROS',NULL,2,5,NULL,1,'2026-05-25 22:01:04',NULL);
INSERT INTO plano_contas VALUES(32,1,'5.3','despesa:energia','A','D',NULL,'DESPESA_OPERACIONAL','INSUMOS',NULL,2,5,NULL,1,'2026-05-25 22:01:04',NULL);
INSERT INTO plano_contas VALUES(33,1,'5.4','despesa:software','A','D',NULL,'DESPESA_OPERACIONAL','CAPITAL_TERCEIROS',NULL,2,5,NULL,1,'2026-05-25 22:01:04',NULL);
INSERT INTO plano_contas VALUES(34,1,'5.5','despesa:contabilidade','A','D',NULL,'DESPESA_OPERACIONAL','CAPITAL_TERCEIROS',NULL,2,5,NULL,1,'2026-05-25 22:01:04',NULL);
INSERT INTO plano_contas VALUES(35,1,'5.6','despesa:prolabore','A','D',NULL,'DESPESA_OPERACIONAL','PESSOAL',NULL,2,5,NULL,1,'2026-05-25 22:01:04',NULL);
INSERT INTO plano_contas VALUES(36,1,'5.7','despesa:inss','A','D',NULL,'DESPESA_OPERACIONAL','PESSOAL',NULL,2,5,NULL,1,'2026-05-25 22:01:04',NULL);
INSERT INTO plano_contas VALUES(37,1,'5.8','despesa:das','A','D',NULL,'DESPESA_OPERACIONAL','IMPOSTOS',NULL,2,5,NULL,1,'2026-05-25 22:01:04',NULL);
INSERT INTO plano_contas VALUES(38,1,'5.9','despesa:iss','A','D',NULL,'DESPESA_OPERACIONAL','IMPOSTOS',NULL,2,5,NULL,1,'2026-05-25 22:01:04',NULL);
INSERT INTO plano_contas VALUES(39,1,'5.10','despesa:tarifas','A','D',NULL,'RESULTADO_FINANCEIRO','CAPITAL_TERCEIROS',NULL,2,5,NULL,1,'2026-05-25 22:01:04',NULL);
INSERT INTO plano_contas VALUES(40,1,'5.11','despesa:juros','A','D',NULL,'RESULTADO_FINANCEIRO','CAPITAL_TERCEIROS',NULL,2,5,NULL,1,'2026-05-25 22:01:04',NULL);
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
INSERT INTO lancamento VALUES(3,1,'2026-06-01','03/2026','receita ref 03/2026','N','2026-06-01 11:42:36',NULL);
INSERT INTO lancamento VALUES(4,1,'2026-06-01',NULL,'registro ISS 03/2026','N','2026-06-01 11:44:36',NULL);
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
INSERT INTO lancamento_item VALUES(5,3,9,'D',20950.0,NULL);
INSERT INTO lancamento_item VALUES(6,3,26,'C',20950.0,NULL);
INSERT INTO lancamento_item VALUES(7,4,38,'D',628.49999999999999998,NULL);
INSERT INTO lancamento_item VALUES(8,4,19,'C',628.49999999999999998,NULL);
CREATE TABLE mapa_demonstracoes (
  id INTEGER PRIMARY KEY AUTOINCREMENT ,
  conta_id INTEGER,
  tipo TEXT, -- DRE, DVA, DFC
  categoria TEXT,
  excluido_at TEXT,

  FOREIGN KEY (conta_id) REFERENCES plano_contas(id)
);
CREATE TABLE tomador (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  cnpj TEXT NOT NULL,
  nome TEXT NOT NULL,
  uf TEXT,
  municipio TEXT,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP,
  excluido_at TEXT
);
INSERT INTO tomador VALUES(1,'88761674000150','EMPRESA SERVICO PRESTADO','CE','Fortaleza','2026-06-01 10:40:50',NULL);
CREATE TABLE trava_contabil (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    empresa_id INTEGER NOT NULL REFERENCES empresa(id),
    ano INTEGER NOT NULL,
    mes INTEGER NOT NULL,
    is_closed INTEGER DEFAULT 0,
    closed_at TEXT
);
INSERT INTO trava_contabil VALUES(1,1,2026,6,0,NULL);
INSERT INTO trava_contabil VALUES(2,1,2026,5,0,NULL);
CREATE TABLE nota_fiscal (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  numero INTEGER,
  codigo TEXT,
  referencia TEXT,
  chave_acesso TEXT,
  situacao TEXT,
  data_emissao TEXT,
  valor_total REAL,
  empresa_id INTEGER,
  tomador_id INTEGER,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP,
  excluido_at TEXT
);
INSERT INTO nota_fiscal VALUES(1,2,'','03/2026','','EMITIDA','2026-05-26',20950.0,1,1,'2026-06-01 11:32:08',NULL);
INSERT INTO nota_fiscal VALUES(2,3,'','04/2026','','EMITIDA','2026-05-26',14249.999999999999999,1,1,'2026-06-01 11:33:08',NULL);
DELETE FROM sqlite_sequence;
INSERT INTO sqlite_sequence VALUES('plano_contas',40);
INSERT INTO sqlite_sequence VALUES('empresa',1);
INSERT INTO sqlite_sequence VALUES('lancamento',4);
INSERT INTO sqlite_sequence VALUES('lancamento_item',8);
INSERT INTO sqlite_sequence VALUES('tomador',1);
INSERT INTO sqlite_sequence VALUES('trava_contabil',2);
INSERT INTO sqlite_sequence VALUES('nota_fiscal',2);
CREATE INDEX idx_lancamento_data ON lancamento(data);
CREATE INDEX idx_lancamento_item_conta ON lancamento_item(conta_id);
COMMIT;
