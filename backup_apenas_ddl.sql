PRAGMA foreign_keys=OFF;
INSERT INTO empresa VALUES(1,'06211011000111','PAOLA LTDA','CE','Fortaleza','2026-05-14',NULL,'2026-05-15 16:47:09',NULL);
INSERT INTO empresa VALUES(2,'02842883288383','alguma outra','CE','fortaleza','2026-05-18',NULL,'2026-05-17 21:42:15',NULL);


-- ============================================================
-- INSERTS: plano_contas_referencial e plano_contas
-- Gerado com base no hledger_plano_contas.txt
-- IDs inteiros explícitos (esquema de numeração hierárquica)
-- ============================================================

-- ============================================================
-- PLANO DE CONTAS REFERENCIAL
-- ============================================================

-- Nível 1 – Grupos principais
INSERT INTO plano_contas_referencial (id, codigo, nome, tipo, natureza, nivel, parent_id, grupo)
VALUES
  (1, '1', 'Ativo',              'S', 'D', 1, NULL, 'ATIVO'),
  (2, '2', 'Passivo',            'S', 'C', 1, NULL, 'PASSIVO'),
  (3, '3', 'Patrimônio Líquido', 'S', 'C', 1, NULL, 'PL'),
  (4, '4', 'Receita',            'S', 'C', 1, NULL, 'RESULTADO'),
  (5, '5', 'Despesa',            'S', 'D', 1, NULL, 'RESULTADO');

-- Nível 2 – Ativo
INSERT INTO plano_contas_referencial (id, codigo, nome, tipo, natureza, nivel, parent_id, grupo)
VALUES
  (11, '1.1', 'Caixa',            'A', 'D', 2, 1, 'ATIVO'),
  (12, '1.2', 'Banco',            'S', 'D', 2, 1, 'ATIVO'),
  (13, '1.3', 'Contas a Receber', 'S', 'D', 2, 1, 'ATIVO'),
  (14, '1.4', 'Imobilizado',      'S', 'D', 2, 1, 'ATIVO');

-- Nível 2 – Passivo
INSERT INTO plano_contas_referencial (id, codigo, nome, tipo, natureza, nivel, parent_id, grupo)
VALUES
  (21, '2.1', 'Fornecedores',        'A', 'C', 2, 2, 'PASSIVO'),
  (22, '2.2', 'Impostos a Recolher', 'S', 'C', 2, 2, 'PASSIVO'),
  (23, '2.3', 'INSS a Recolher',     'A', 'C', 2, 2, 'PASSIVO'),
  (24, '2.4', 'Pró-labore a Pagar',  'A', 'C', 2, 2, 'PASSIVO');

-- Nível 2 – Patrimônio Líquido
INSERT INTO plano_contas_referencial (id, codigo, nome, tipo, natureza, nivel, parent_id, grupo)
VALUES
  (31, '3.1', 'Capital Social',        'A', 'C', 2, 3, 'PL'),
  (32, '3.2', 'Lucros Acumulados',     'A', 'C', 2, 3, 'PL'),
  (33, '3.3', 'Distribuição de Lucros','A', 'C', 2, 3, 'PL');

-- Nível 2 – Receita
INSERT INTO plano_contas_referencial (id, codigo, nome, tipo, natureza, nivel, parent_id, grupo, dre_grupo)
VALUES
  (41, '4.1', 'Receita de Plantão',     'S', 'C', 2, 4, 'RESULTADO', 'RECEITA_BRUTA'),
  (42, '4.2', 'Receita de Consultas',   'A', 'C', 2, 4, 'RESULTADO', 'RECEITA_BRUTA'),
  (43, '4.3', 'Rendimentos Financeiros','A', 'C', 2, 4, 'RESULTADO', 'RECEITA_FINANCEIRA');

-- Nível 2 – Despesa
INSERT INTO plano_contas_referencial (id, codigo, nome, tipo, natureza, nivel, parent_id, grupo, dre_grupo)
VALUES
  (51,  '5.1',  'Aluguel',          'A', 'D', 2, 5, 'RESULTADO', 'DESPESA_OPERACIONAL'),
  (52,  '5.2',  'Internet',         'A', 'D', 2, 5, 'RESULTADO', 'DESPESA_OPERACIONAL'),
  (53,  '5.3',  'Energia',          'A', 'D', 2, 5, 'RESULTADO', 'DESPESA_OPERACIONAL'),
  (54,  '5.4',  'Software',         'A', 'D', 2, 5, 'RESULTADO', 'DESPESA_OPERACIONAL'),
  (55,  '5.5',  'Contabilidade',    'A', 'D', 2, 5, 'RESULTADO', 'DESPESA_OPERACIONAL'),
  (56,  '5.6',  'Pró-labore',       'A', 'D', 2, 5, 'RESULTADO', 'DESPESA_PESSOAL'),
  (57,  '5.7',  'INSS',             'A', 'D', 2, 5, 'RESULTADO', 'DESPESA_PESSOAL'),
  (58,  '5.8',  'DAS',              'A', 'D', 2, 5, 'RESULTADO', 'DESPESA_TRIBUTARIA'),
  (59,  '5.9',  'ISS',              'A', 'D', 2, 5, 'RESULTADO', 'DESPESA_TRIBUTARIA'),
  (510, '5.10', 'Tarifas Bancárias','A', 'D', 2, 5, 'RESULTADO', 'DESPESA_FINANCEIRA'),
  (511, '5.11', 'Juros',            'A', 'D', 2, 5, 'RESULTADO', 'DESPESA_FINANCEIRA');

-- Nível 3 – Banco
INSERT INTO plano_contas_referencial (id, codigo, nome, tipo, natureza, nivel, parent_id, grupo)
VALUES
  (121, '1.2.1', 'Conta Corrente', 'A', 'D', 3, 12, 'ATIVO'),
  (122, '1.2.2', 'Conta Digital',  'A', 'D', 3, 12, 'ATIVO');

-- Nível 3 – Contas a Receber
INSERT INTO plano_contas_referencial (id, codigo, nome, tipo, natureza, nivel, parent_id, grupo)
VALUES
  (131, '1.3.1', 'Hospital A', 'A', 'D', 3, 13, 'ATIVO'),
  (132, '1.3.2', 'Hospital B', 'A', 'D', 3, 13, 'ATIVO');

-- Nível 3 – Imobilizado
INSERT INTO plano_contas_referencial (id, codigo, nome, tipo, natureza, nivel, parent_id, grupo)
VALUES
  (141, '1.4.1', 'Equipamentos', 'A', 'D', 3, 14, 'ATIVO'),
  (142, '1.4.2', 'Computadores', 'A', 'D', 3, 14, 'ATIVO');

-- Nível 3 – Impostos (Passivo)
INSERT INTO plano_contas_referencial (id, codigo, nome, tipo, natureza, nivel, parent_id, grupo)
VALUES
  (221, '2.2.1', 'DAS a Recolher', 'A', 'C', 3, 22, 'PASSIVO'),
  (222, '2.2.2', 'ISS a Recolher', 'A', 'C', 3, 22, 'PASSIVO');

-- Nível 3 – Receita de Plantão
INSERT INTO plano_contas_referencial (id, codigo, nome, tipo, natureza, nivel, parent_id, grupo, dre_grupo)
VALUES
  (411, '4.1.1', 'Plantão Hospital A', 'A', 'C', 3, 41, 'RESULTADO', 'RECEITA_BRUTA'),
  (412, '4.1.2', 'Plantão Hospital B', 'A', 'C', 3, 41, 'RESULTADO', 'RECEITA_BRUTA');

-- ============================================================
-- PLANO DE CONTAS (espelha o referencial sem empresa específica)
-- conta_pai_id resolvido via subquery no codigo
-- aceita_lancamento: 0 = sintética, 1 = analítica
-- ============================================================

-- Nível 1
INSERT INTO plano_contas (plano_contas_referencial_id, codigo, descricao, tipo, natureza, nivel, conta_pai_id, codigo_referencial, grupo, aceita_lancamento)
VALUES
  (1, '1', 'Ativo',              'S', 'D', 1, NULL, '1', 'ATIVO',     0),
  (2, '2', 'Passivo',            'S', 'C', 1, NULL, '2', 'PASSIVO',   0),
  (3, '3', 'Patrimônio Líquido', 'S', 'C', 1, NULL, '3', 'PL',        0),
  (4, '4', 'Receita',            'S', 'C', 1, NULL, '4', 'RESULTADO', 0),
  (5, '5', 'Despesa',            'S', 'D', 1, NULL, '5', 'RESULTADO', 0);

-- Nível 2 – Ativo
INSERT INTO plano_contas (plano_contas_referencial_id, codigo, descricao, tipo, natureza, nivel, conta_pai_id, codigo_referencial, grupo, aceita_lancamento)
SELECT 11, '1.1', 'Caixa',            'A', 'D', 2, id, '1.1', 'ATIVO', 1 FROM plano_contas WHERE codigo = '1';
INSERT INTO plano_contas (plano_contas_referencial_id, codigo, descricao, tipo, natureza, nivel, conta_pai_id, codigo_referencial, grupo, aceita_lancamento)
SELECT 12, '1.2', 'Banco',            'S', 'D', 2, id, '1.2', 'ATIVO', 0 FROM plano_contas WHERE codigo = '1';
INSERT INTO plano_contas (plano_contas_referencial_id, codigo, descricao, tipo, natureza, nivel, conta_pai_id, codigo_referencial, grupo, aceita_lancamento)
SELECT 13, '1.3', 'Contas a Receber', 'S', 'D', 2, id, '1.3', 'ATIVO', 0 FROM plano_contas WHERE codigo = '1';
INSERT INTO plano_contas (plano_contas_referencial_id, codigo, descricao, tipo, natureza, nivel, conta_pai_id, codigo_referencial, grupo, aceita_lancamento)
SELECT 14, '1.4', 'Imobilizado',      'S', 'D', 2, id, '1.4', 'ATIVO', 0 FROM plano_contas WHERE codigo = '1';

-- Nível 2 – Passivo
INSERT INTO plano_contas (plano_contas_referencial_id, codigo, descricao, tipo, natureza, nivel, conta_pai_id, codigo_referencial, grupo, aceita_lancamento)
SELECT 21, '2.1', 'Fornecedores',        'A', 'C', 2, id, '2.1', 'PASSIVO', 1 FROM plano_contas WHERE codigo = '2';
INSERT INTO plano_contas (plano_contas_referencial_id, codigo, descricao, tipo, natureza, nivel, conta_pai_id, codigo_referencial, grupo, aceita_lancamento)
SELECT 22, '2.2', 'Impostos a Recolher', 'S', 'C', 2, id, '2.2', 'PASSIVO', 0 FROM plano_contas WHERE codigo = '2';
INSERT INTO plano_contas (plano_contas_referencial_id, codigo, descricao, tipo, natureza, nivel, conta_pai_id, codigo_referencial, grupo, aceita_lancamento)
SELECT 23, '2.3', 'INSS a Recolher',     'A', 'C', 2, id, '2.3', 'PASSIVO', 1 FROM plano_contas WHERE codigo = '2';
INSERT INTO plano_contas (plano_contas_referencial_id, codigo, descricao, tipo, natureza, nivel, conta_pai_id, codigo_referencial, grupo, aceita_lancamento)
SELECT 24, '2.4', 'Pró-labore a Pagar',  'A', 'C', 2, id, '2.4', 'PASSIVO', 1 FROM plano_contas WHERE codigo = '2';

-- Nível 2 – Patrimônio Líquido
INSERT INTO plano_contas (plano_contas_referencial_id, codigo, descricao, tipo, natureza, nivel, conta_pai_id, codigo_referencial, grupo, aceita_lancamento)
SELECT 31, '3.1', 'Capital Social',        'A', 'C', 2, id, '3.1', 'PL', 1 FROM plano_contas WHERE codigo = '3';
INSERT INTO plano_contas (plano_contas_referencial_id, codigo, descricao, tipo, natureza, nivel, conta_pai_id, codigo_referencial, grupo, aceita_lancamento)
SELECT 32, '3.2', 'Lucros Acumulados',     'A', 'C', 2, id, '3.2', 'PL', 1 FROM plano_contas WHERE codigo = '3';
INSERT INTO plano_contas (plano_contas_referencial_id, codigo, descricao, tipo, natureza, nivel, conta_pai_id, codigo_referencial, grupo, aceita_lancamento)
SELECT 33, '3.3', 'Distribuição de Lucros','A', 'C', 2, id, '3.3', 'PL', 1 FROM plano_contas WHERE codigo = '3';

-- Nível 2 – Receita
INSERT INTO plano_contas (plano_contas_referencial_id, codigo, descricao, tipo, natureza, nivel, conta_pai_id, codigo_referencial, grupo, dre_grupo, aceita_lancamento)
SELECT 41, '4.1', 'Receita de Plantão',     'S', 'C', 2, id, '4.1', 'RESULTADO', 'RECEITA_BRUTA',     0 FROM plano_contas WHERE codigo = '4';
INSERT INTO plano_contas (plano_contas_referencial_id, codigo, descricao, tipo, natureza, nivel, conta_pai_id, codigo_referencial, grupo, dre_grupo, aceita_lancamento)
SELECT 42, '4.2', 'Receita de Consultas',   'A', 'C', 2, id, '4.2', 'RESULTADO', 'RECEITA_BRUTA',     1 FROM plano_contas WHERE codigo = '4';
INSERT INTO plano_contas (plano_contas_referencial_id, codigo, descricao, tipo, natureza, nivel, conta_pai_id, codigo_referencial, grupo, dre_grupo, aceita_lancamento)
SELECT 43, '4.3', 'Rendimentos Financeiros','A', 'C', 2, id, '4.3', 'RESULTADO', 'RECEITA_FINANCEIRA', 1 FROM plano_contas WHERE codigo = '4';

-- Nível 2 – Despesa
INSERT INTO plano_contas (plano_contas_referencial_id, codigo, descricao, tipo, natureza, nivel, conta_pai_id, codigo_referencial, grupo, dre_grupo, aceita_lancamento)
SELECT 51,  '5.1',  'Aluguel',          'A', 'D', 2, id, '5.1',  'RESULTADO', 'DESPESA_OPERACIONAL', 1 FROM plano_contas WHERE codigo = '5';
INSERT INTO plano_contas (plano_contas_referencial_id, codigo, descricao, tipo, natureza, nivel, conta_pai_id, codigo_referencial, grupo, dre_grupo, aceita_lancamento)
SELECT 52,  '5.2',  'Internet',         'A', 'D', 2, id, '5.2',  'RESULTADO', 'DESPESA_OPERACIONAL', 1 FROM plano_contas WHERE codigo = '5';
INSERT INTO plano_contas (plano_contas_referencial_id, codigo, descricao, tipo, natureza, nivel, conta_pai_id, codigo_referencial, grupo, dre_grupo, aceita_lancamento)
SELECT 53,  '5.3',  'Energia',          'A', 'D', 2, id, '5.3',  'RESULTADO', 'DESPESA_OPERACIONAL', 1 FROM plano_contas WHERE codigo = '5';
INSERT INTO plano_contas (plano_contas_referencial_id, codigo, descricao, tipo, natureza, nivel, conta_pai_id, codigo_referencial, grupo, dre_grupo, aceita_lancamento)
SELECT 54,  '5.4',  'Software',         'A', 'D', 2, id, '5.4',  'RESULTADO', 'DESPESA_OPERACIONAL', 1 FROM plano_contas WHERE codigo = '5';
INSERT INTO plano_contas (plano_contas_referencial_id, codigo, descricao, tipo, natureza, nivel, conta_pai_id, codigo_referencial, grupo, dre_grupo, aceita_lancamento)
SELECT 55,  '5.5',  'Contabilidade',    'A', 'D', 2, id, '5.5',  'RESULTADO', 'DESPESA_OPERACIONAL', 1 FROM plano_contas WHERE codigo = '5';
INSERT INTO plano_contas (plano_contas_referencial_id, codigo, descricao, tipo, natureza, nivel, conta_pai_id, codigo_referencial, grupo, dre_grupo, aceita_lancamento)
SELECT 56,  '5.6',  'Pró-labore',       'A', 'D', 2, id, '5.6',  'RESULTADO', 'DESPESA_PESSOAL',    1 FROM plano_contas WHERE codigo = '5';
INSERT INTO plano_contas (plano_contas_referencial_id, codigo, descricao, tipo, natureza, nivel, conta_pai_id, codigo_referencial, grupo, dre_grupo, aceita_lancamento)
SELECT 57,  '5.7',  'INSS',             'A', 'D', 2, id, '5.7',  'RESULTADO', 'DESPESA_PESSOAL',    1 FROM plano_contas WHERE codigo = '5';
INSERT INTO plano_contas (plano_contas_referencial_id, codigo, descricao, tipo, natureza, nivel, conta_pai_id, codigo_referencial, grupo, dre_grupo, aceita_lancamento)
SELECT 58,  '5.8',  'DAS',              'A', 'D', 2, id, '5.8',  'RESULTADO', 'DESPESA_TRIBUTARIA', 1 FROM plano_contas WHERE codigo = '5';
INSERT INTO plano_contas (plano_contas_referencial_id, codigo, descricao, tipo, natureza, nivel, conta_pai_id, codigo_referencial, grupo, dre_grupo, aceita_lancamento)
SELECT 59,  '5.9',  'ISS',              'A', 'D', 2, id, '5.9',  'RESULTADO', 'DESPESA_TRIBUTARIA', 1 FROM plano_contas WHERE codigo = '5';
INSERT INTO plano_contas (plano_contas_referencial_id, codigo, descricao, tipo, natureza, nivel, conta_pai_id, codigo_referencial, grupo, dre_grupo, aceita_lancamento)
SELECT 510, '5.10', 'Tarifas Bancárias','A', 'D', 2, id, '5.10', 'RESULTADO', 'DESPESA_FINANCEIRA', 1 FROM plano_contas WHERE codigo = '5';
INSERT INTO plano_contas (plano_contas_referencial_id, codigo, descricao, tipo, natureza, nivel, conta_pai_id, codigo_referencial, grupo, dre_grupo, aceita_lancamento)
SELECT 511, '5.11', 'Juros',            'A', 'D', 2, id, '5.11', 'RESULTADO', 'DESPESA_FINANCEIRA', 1 FROM plano_contas WHERE codigo = '5';

-- Nível 3 – Banco
INSERT INTO plano_contas (plano_contas_referencial_id, codigo, descricao, tipo, natureza, nivel, conta_pai_id, codigo_referencial, grupo, aceita_lancamento)
SELECT 121, '1.2.1', 'Conta Corrente', 'A', 'D', 3, id, '1.2.1', 'ATIVO', 1 FROM plano_contas WHERE codigo = '1.2';
INSERT INTO plano_contas (plano_contas_referencial_id, codigo, descricao, tipo, natureza, nivel, conta_pai_id, codigo_referencial, grupo, aceita_lancamento)
SELECT 122, '1.2.2', 'Conta Digital',  'A', 'D', 3, id, '1.2.2', 'ATIVO', 1 FROM plano_contas WHERE codigo = '1.2';

-- Nível 3 – Contas a Receber
INSERT INTO plano_contas (plano_contas_referencial_id, codigo, descricao, tipo, natureza, nivel, conta_pai_id, codigo_referencial, grupo, aceita_lancamento)
SELECT 131, '1.3.1', 'Hospital A', 'A', 'D', 3, id, '1.3.1', 'ATIVO', 1 FROM plano_contas WHERE codigo = '1.3';
INSERT INTO plano_contas (plano_contas_referencial_id, codigo, descricao, tipo, natureza, nivel, conta_pai_id, codigo_referencial, grupo, aceita_lancamento)
SELECT 132, '1.3.2', 'Hospital B', 'A', 'D', 3, id, '1.3.2', 'ATIVO', 1 FROM plano_contas WHERE codigo = '1.3';

-- Nível 3 – Imobilizado
INSERT INTO plano_contas (plano_contas_referencial_id, codigo, descricao, tipo, natureza, nivel, conta_pai_id, codigo_referencial, grupo, aceita_lancamento)
SELECT 141, '1.4.1', 'Equipamentos', 'A', 'D', 3, id, '1.4.1', 'ATIVO', 1 FROM plano_contas WHERE codigo = '1.4';
INSERT INTO plano_contas (plano_contas_referencial_id, codigo, descricao, tipo, natureza, nivel, conta_pai_id, codigo_referencial, grupo, aceita_lancamento)
SELECT 142, '1.4.2', 'Computadores', 'A', 'D', 3, id, '1.4.2', 'ATIVO', 1 FROM plano_contas WHERE codigo = '1.4';

-- Nível 3 – Impostos (Passivo)
INSERT INTO plano_contas (plano_contas_referencial_id, codigo, descricao, tipo, natureza, nivel, conta_pai_id, codigo_referencial, grupo, aceita_lancamento)
SELECT 221, '2.2.1', 'DAS a Recolher', 'A', 'C', 3, id, '2.2.1', 'PASSIVO', 1 FROM plano_contas WHERE codigo = '2.2';
INSERT INTO plano_contas (plano_contas_referencial_id, codigo, descricao, tipo, natureza, nivel, conta_pai_id, codigo_referencial, grupo, aceita_lancamento)
SELECT 222, '2.2.2', 'ISS a Recolher', 'A', 'C', 3, id, '2.2.2', 'PASSIVO', 1 FROM plano_contas WHERE codigo = '2.2';

-- Nível 3 – Receita de Plantão
INSERT INTO plano_contas (plano_contas_referencial_id, codigo, descricao, tipo, natureza, nivel, conta_pai_id, codigo_referencial, grupo, dre_grupo, aceita_lancamento)
SELECT 411, '4.1.1', 'Plantão Hospital A', 'A', 'C', 3, id, '4.1.1', 'RESULTADO', 'RECEITA_BRUTA', 1 FROM plano_contas WHERE codigo = '4.1';
INSERT INTO plano_contas (plano_contas_referencial_id, codigo, descricao, tipo, natureza, nivel, conta_pai_id, codigo_referencial, grupo, dre_grupo, aceita_lancamento)
SELECT 412, '4.1.2', 'Plantão Hospital B', 'A', 'C', 3, id, '4.1.2', 'RESULTADO', 'RECEITA_BRUTA', 1 FROM plano_contas WHERE codigo = '4.1';
INSERT INTO lancamento VALUES(1,1,'2026-05-19',NULL,'alguma coisa','N','2026-05-19 16:03:17',NULL);

INSERT INTO lancamento_item VALUES(1,1,8,'D',3000.0,NULL);
INSERT INTO lancamento_item VALUES(2,1,29,'C',3000.0,NULL);

INSERT INTO report_types VALUES('4ba4448ae0c0739f57f901cb9ce4e28b','BALANCO','Balanço Patrimonial');
INSERT INTO report_types VALUES('a0b2b220151acf28a4cb6efc6e612fb0','DRE','Demonstração do Resultado');
INSERT INTO report_types VALUES('a2a97dc9ddeb09f2e9a7f43c76a1a99f','DFC','Demonstração do Fluxo de Caixa');
INSERT INTO report_types VALUES('0bcc1c1ae84165dcfba15d1334d0f698','DVA','Demonstração do Valor Adicionado');
INSERT INTO report_types VALUES('fce957ddccf07cb5dd71c0c2a663ea63','BALANCETE','Balancete');

INSERT INTO regras VALUES('e61bfc126115b1c40592f72d1ed179ef','SUPER_ADMIN','Super Administrador');
INSERT INTO regras VALUES('1f45652cda4b95c0cf9a227492aaf735','ACCOUNTANT','Contador');
INSERT INTO regras VALUES('e5087a4c741fad9a8204bd4c27114524','ASSISTANT','Assistente Contábil');
INSERT INTO regras VALUES('55a805c9e909b2a35781fb25a407e3b9','AUDITOR','Auditor');
INSERT INTO regras VALUES('3257c755155a818f9405865671523bc5','CLIENT','Cliente');

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

INSERT INTO sped_natureza VALUES('b0f9d18cad046481f904147472bc12cf','01','Contas de Ativo');
INSERT INTO sped_natureza VALUES('b6dc5d9e892bd44eb22b47edb66697d6','02','Contas de Passivo');
INSERT INTO sped_natureza VALUES('19f89a94e009390272bb852854638378','03','Patrimônio Líquido');
INSERT INTO sped_natureza VALUES('f71c8713afb40d53f5cde056a3ac37ef','04','Receitas');
INSERT INTO sped_natureza VALUES('cd3633b4ea01a23d9e794966ebde0407','05','Custos');
INSERT INTO sped_natureza VALUES('17548147635eedb6ec7969515d48d7bb','06','Despesas');

DELETE FROM sqlite_sequence;
INSERT INTO sqlite_sequence VALUES('plano_contas',40);
INSERT INTO sqlite_sequence VALUES('empresa',2);
INSERT INTO sqlite_sequence VALUES('lancamento',1);
INSERT INTO sqlite_sequence VALUES('lancamento_item',2);
