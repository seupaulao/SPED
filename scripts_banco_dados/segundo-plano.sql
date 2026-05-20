-- Script de insercao: Segundo Plano de Contas
-- Modelo baseado em hledger para escritorio contabil (medico PJ)
-- Estrutura derivada de plano_contas_simples.txt

-- Observacao: este script assume empresa_id = 1
-- Se precisar para outra empresa, substitua o valor de empresa_id

-- ====================================================================
-- CONTAS RAIZ (SINTETICAS - NIVEL 1)
-- ====================================================================

-- 1. ATIVO
INSERT INTO plano_contas (
  empresa_id, codigo, descricao, tipo, natureza, grupo, nivel,
  conta_pai_id, aceita_lancamento
) VALUES (
  1, '1', 'ativo', 'S', 'D', 'ATIVO', 1, NULL, 0
);

-- 2. PASSIVO
INSERT INTO plano_contas (
  empresa_id, codigo, descricao, tipo, natureza, grupo, nivel,
  conta_pai_id, aceita_lancamento
) VALUES (
  1, '2', 'passivo', 'S', 'C', 'PASSIVO', 1, NULL, 0
);

-- 3. PATRIMONIOLIQUIDO
INSERT INTO plano_contas (
  empresa_id, codigo, descricao, tipo, natureza, grupo, nivel,
  conta_pai_id, aceita_lancamento
) VALUES (
  1, '3', 'patrimonioliquido', 'S', 'C', 'PL', 1, NULL, 0
);

-- 4. RECEITA
INSERT INTO plano_contas (
  empresa_id, codigo, descricao, tipo, natureza, dre_grupo, nivel,
  conta_pai_id, aceita_lancamento
) VALUES (
  1, '4', 'receita', 'S', 'C', 'RECEITA_BRUTA', 1, NULL, 0
);

-- 5. DESPESA
INSERT INTO plano_contas (
  empresa_id, codigo, descricao, tipo, natureza, nivel,
  conta_pai_id, aceita_lancamento
) VALUES (
  1, '5', 'despesa', 'S', 'D', 1, NULL, 0
);

-- ====================================================================
-- SUBCONTAS DE ATIVO
-- ====================================================================

-- 1.1 Caixa
INSERT INTO plano_contas (
  empresa_id, codigo, descricao, tipo, natureza, grupo, nivel,
  conta_pai_id, aceita_lancamento
) VALUES (
  1, '1.1', 'ativo:caixa', 'A', 'D', 'ATIVO', 2,
  (SELECT id FROM plano_contas WHERE empresa_id=1 AND codigo='1'), 1
);

-- 1.2 Banco
INSERT INTO plano_contas (
  empresa_id, codigo, descricao, tipo, natureza, grupo, nivel,
  conta_pai_id, aceita_lancamento
) VALUES (
  1, '1.2', 'ativo:banco', 'S', 'D', 'ATIVO', 2,
  (SELECT id FROM plano_contas WHERE empresa_id=1 AND codigo='1'), 0
);

-- 1.2.1 Conta Corrente
INSERT INTO plano_contas (
  empresa_id, codigo, descricao, tipo, natureza, grupo, nivel,
  conta_pai_id, aceita_lancamento
) VALUES (
  1, '1.2.1', 'ativo:banco:conta_corrente', 'A', 'D', 'ATIVO', 3,
  (SELECT id FROM plano_contas WHERE empresa_id=1 AND codigo='1.2'), 1
);

-- 1.2.2 Conta Digital
INSERT INTO plano_contas (
  empresa_id, codigo, descricao, tipo, natureza, grupo, nivel,
  conta_pai_id, aceita_lancamento
) VALUES (
  1, '1.2.2', 'ativo:banco:conta_digital', 'A', 'D', 'ATIVO', 3,
  (SELECT id FROM plano_contas WHERE empresa_id=1 AND codigo='1.2'), 1
);

-- 1.3 Contas a Receber
INSERT INTO plano_contas (
  empresa_id, codigo, descricao, tipo, natureza, grupo, nivel,
  conta_pai_id, aceita_lancamento
) VALUES (
  1, '1.3', 'ativo:contas_a_receber', 'S', 'D', 'ATIVO', 2,
  (SELECT id FROM plano_contas WHERE empresa_id=1 AND codigo='1'), 0
);

-- 1.3.1 Hospital A
INSERT INTO plano_contas (
  empresa_id, codigo, descricao, tipo, natureza, grupo, nivel,
  conta_pai_id, aceita_lancamento
) VALUES (
  1, '1.3.1', 'ativo:contas_a_receber:hospital_a', 'A', 'D', 'ATIVO', 3,
  (SELECT id FROM plano_contas WHERE empresa_id=1 AND codigo='1.3'), 1
);

-- 1.3.2 Hospital B
INSERT INTO plano_contas (
  empresa_id, codigo, descricao, tipo, natureza, grupo, nivel,
  conta_pai_id, aceita_lancamento
) VALUES (
  1, '1.3.2', 'ativo:contas_a_receber:hospital_b', 'A', 'D', 'ATIVO', 3,
  (SELECT id FROM plano_contas WHERE empresa_id=1 AND codigo='1.3'), 1
);

-- 1.4 Imobilizado
INSERT INTO plano_contas (
  empresa_id, codigo, descricao, tipo, natureza, grupo, nivel,
  conta_pai_id, aceita_lancamento
) VALUES (
  1, '1.4', 'ativo:imobilizado', 'S', 'D', 'ATIVO', 2,
  (SELECT id FROM plano_contas WHERE empresa_id=1 AND codigo='1'), 0
);

-- 1.4.1 Equipamentos
INSERT INTO plano_contas (
  empresa_id, codigo, descricao, tipo, natureza, grupo, nivel,
  conta_pai_id, aceita_lancamento
) VALUES (
  1, '1.4.1', 'ativo:imobilizado:equipamentos', 'A', 'D', 'ATIVO', 3,
  (SELECT id FROM plano_contas WHERE empresa_id=1 AND codigo='1.4'), 1
);

-- 1.4.2 Computadores
INSERT INTO plano_contas (
  empresa_id, codigo, descricao, tipo, natureza, grupo, nivel,
  conta_pai_id, aceita_lancamento
) VALUES (
  1, '1.4.2', 'ativo:imobilizado:computadores', 'A', 'D', 'ATIVO', 3,
  (SELECT id FROM plano_contas WHERE empresa_id=1 AND codigo='1.4'), 1
);

-- ====================================================================
-- SUBCONTAS DE PASSIVO
-- ====================================================================

-- 2.1 Fornecedores
INSERT INTO plano_contas (
  empresa_id, codigo, descricao, tipo, natureza, grupo, nivel,
  conta_pai_id, aceita_lancamento
) VALUES (
  1, '2.1', 'passivo:fornecedores', 'A', 'C', 'PASSIVO', 2,
  (SELECT id FROM plano_contas WHERE empresa_id=1 AND codigo='2'), 1
);

-- 2.2 Impostos
INSERT INTO plano_contas (
  empresa_id, codigo, descricao, tipo, natureza, grupo, nivel,
  conta_pai_id, aceita_lancamento
) VALUES (
  1, '2.2', 'passivo:impostos', 'S', 'C', 'PASSIVO', 2,
  (SELECT id FROM plano_contas WHERE empresa_id=1 AND codigo='2'), 0
);

-- 2.2.1 DAS
INSERT INTO plano_contas (
  empresa_id, codigo, descricao, tipo, natureza, grupo, nivel,
  conta_pai_id, aceita_lancamento
) VALUES (
  1, '2.2.1', 'passivo:impostos:das', 'A', 'C', 'PASSIVO', 3,
  (SELECT id FROM plano_contas WHERE empresa_id=1 AND codigo='2.2'), 1
);

-- 2.2.2 ISS
INSERT INTO plano_contas (
  empresa_id, codigo, descricao, tipo, natureza, grupo, nivel,
  conta_pai_id, aceita_lancamento
) VALUES (
  1, '2.2.2', 'passivo:impostos:iss', 'A', 'C', 'PASSIVO', 3,
  (SELECT id FROM plano_contas WHERE empresa_id=1 AND codigo='2.2'), 1
);

-- 2.3 INSS
INSERT INTO plano_contas (
  empresa_id, codigo, descricao, tipo, natureza, grupo, nivel,
  conta_pai_id, aceita_lancamento
) VALUES (
  1, '2.3', 'passivo:inss', 'A', 'C', 'PASSIVO', 2,
  (SELECT id FROM plano_contas WHERE empresa_id=1 AND codigo='2'), 1
);

-- 2.4 Pro Labore
INSERT INTO plano_contas (
  empresa_id, codigo, descricao, tipo, natureza, grupo, nivel,
  conta_pai_id, aceita_lancamento
) VALUES (
  1, '2.4', 'passivo:prolabore', 'A', 'C', 'PASSIVO', 2,
  (SELECT id FROM plano_contas WHERE empresa_id=1 AND codigo='2'), 1
);

-- ====================================================================
-- SUBCONTAS DE PATRIMONIOLIQUIDO
-- ====================================================================

-- 3.1 Capital Social
INSERT INTO plano_contas (
  empresa_id, codigo, descricao, tipo, natureza, grupo, nivel,
  conta_pai_id, aceita_lancamento
) VALUES (
  1, '3.1', 'patrimonioliquido:capital_social', 'A', 'C', 'PL', 2,
  (SELECT id FROM plano_contas WHERE empresa_id=1 AND codigo='3'), 1
);

-- 3.2 Lucros Acumulados
INSERT INTO plano_contas (
  empresa_id, codigo, descricao, tipo, natureza, grupo, nivel,
  conta_pai_id, aceita_lancamento
) VALUES (
  1, '3.2', 'patrimonioliquido:lucros_acumulados', 'A', 'C', 'PL', 2,
  (SELECT id FROM plano_contas WHERE empresa_id=1 AND codigo='3'), 1
);

-- 3.3 Distribuicao de Lucros
INSERT INTO plano_contas (
  empresa_id, codigo, descricao, tipo, natureza, grupo, nivel,
  conta_pai_id, aceita_lancamento
) VALUES (
  1, '3.3', 'patrimonioliquido:distribuicao_lucros', 'A', 'C', 'PL', 2,
  (SELECT id FROM plano_contas WHERE empresa_id=1 AND codigo='3'), 1
);

-- ====================================================================
-- SUBCONTAS DE RECEITA
-- ====================================================================

-- 4.1 Plantao
INSERT INTO plano_contas (
  empresa_id, codigo, descricao, tipo, natureza, dre_grupo, nivel,
  conta_pai_id, aceita_lancamento
) VALUES (
  1, '4.1', 'receita:plantao', 'S', 'C', 'RECEITA_BRUTA', 2,
  (SELECT id FROM plano_contas WHERE empresa_id=1 AND codigo='4'), 0
);

-- 4.1.1 Hospital A
INSERT INTO plano_contas (
  empresa_id, codigo, descricao, tipo, natureza, dre_grupo, subgrupo, nivel,
  conta_pai_id, aceita_lancamento
) VALUES (
  1, '4.1.1', 'receita:plantao:hospital_a', 'A', 'C', 'RECEITA_BRUTA', 'RECEITAS', 3,
  (SELECT id FROM plano_contas WHERE empresa_id=1 AND codigo='4.1'), 1
);

-- 4.1.2 Hospital B
INSERT INTO plano_contas (
  empresa_id, codigo, descricao, tipo, natureza, dre_grupo, subgrupo, nivel,
  conta_pai_id, aceita_lancamento
) VALUES (
  1, '4.1.2', 'receita:plantao:hospital_b', 'A', 'C', 'RECEITA_BRUTA', 'RECEITAS', 3,
  (SELECT id FROM plano_contas WHERE empresa_id=1 AND codigo='4.1'), 1
);

-- 4.2 Consultas
INSERT INTO plano_contas (
  empresa_id, codigo, descricao, tipo, natureza, dre_grupo, subgrupo, nivel,
  conta_pai_id, aceita_lancamento
) VALUES (
  1, '4.2', 'receita:consultas', 'A', 'C', 'RECEITA_BRUTA', 'RECEITAS', 2,
  (SELECT id FROM plano_contas WHERE empresa_id=1 AND codigo='4'), 1
);

-- 4.3 Rendimentos
INSERT INTO plano_contas (
  empresa_id, codigo, descricao, tipo, natureza, dre_grupo, subgrupo, nivel,
  conta_pai_id, aceita_lancamento
) VALUES (
  1, '4.3', 'receita:rendimentos', 'A', 'C', 'RECEITA_BRUTA', 'RECEITAS', 2,
  (SELECT id FROM plano_contas WHERE empresa_id=1 AND codigo='4'), 1
);

-- ====================================================================
-- SUBCONTAS DE DESPESA
-- ====================================================================

-- 5.1 Aluguel
INSERT INTO plano_contas (
  empresa_id, codigo, descricao, tipo, natureza, dre_grupo, subgrupo, nivel,
  conta_pai_id, aceita_lancamento
) VALUES (
  1, '5.1', 'despesa:aluguel', 'A', 'D', 'DESPESA_OPERACIONAL', 'CAPITAL_TERCEIROS', 2,
  (SELECT id FROM plano_contas WHERE empresa_id=1 AND codigo='5'), 1
);

-- 5.2 Internet
INSERT INTO plano_contas (
  empresa_id, codigo, descricao, tipo, natureza, dre_grupo, subgrupo, nivel,
  conta_pai_id, aceita_lancamento
) VALUES (
  1, '5.2', 'despesa:internet', 'A', 'D', 'DESPESA_OPERACIONAL', 'CAPITAL_TERCEIROS', 2,
  (SELECT id FROM plano_contas WHERE empresa_id=1 AND codigo='5'), 1
);

-- 5.3 Energia
INSERT INTO plano_contas (
  empresa_id, codigo, descricao, tipo, natureza, dre_grupo, subgrupo, nivel,
  conta_pai_id, aceita_lancamento
) VALUES (
  1, '5.3', 'despesa:energia', 'A', 'D', 'DESPESA_OPERACIONAL', 'INSUMOS', 2,
  (SELECT id FROM plano_contas WHERE empresa_id=1 AND codigo='5'), 1
);

-- 5.4 Software
INSERT INTO plano_contas (
  empresa_id, codigo, descricao, tipo, natureza, dre_grupo, subgrupo, nivel,
  conta_pai_id, aceita_lancamento
) VALUES (
  1, '5.4', 'despesa:software', 'A', 'D', 'DESPESA_OPERACIONAL', 'CAPITAL_TERCEIROS', 2,
  (SELECT id FROM plano_contas WHERE empresa_id=1 AND codigo='5'), 1
);

-- 5.5 Contabilidade
INSERT INTO plano_contas (
  empresa_id, codigo, descricao, tipo, natureza, dre_grupo, subgrupo, nivel,
  conta_pai_id, aceita_lancamento
) VALUES (
  1, '5.5', 'despesa:contabilidade', 'A', 'D', 'DESPESA_OPERACIONAL', 'CAPITAL_TERCEIROS', 2,
  (SELECT id FROM plano_contas WHERE empresa_id=1 AND codigo='5'), 1
);

-- 5.6 Pro Labore
INSERT INTO plano_contas (
  empresa_id, codigo, descricao, tipo, natureza, dre_grupo, subgrupo, nivel,
  conta_pai_id, aceita_lancamento
) VALUES (
  1, '5.6', 'despesa:prolabore', 'A', 'D', 'DESPESA_OPERACIONAL', 'PESSOAL', 2,
  (SELECT id FROM plano_contas WHERE empresa_id=1 AND codigo='5'), 1
);

-- 5.7 INSS
INSERT INTO plano_contas (
  empresa_id, codigo, descricao, tipo, natureza, dre_grupo, subgrupo, nivel,
  conta_pai_id, aceita_lancamento
) VALUES (
  1, '5.7', 'despesa:inss', 'A', 'D', 'DESPESA_OPERACIONAL', 'PESSOAL', 2,
  (SELECT id FROM plano_contas WHERE empresa_id=1 AND codigo='5'), 1
);

-- 5.8 DAS
INSERT INTO plano_contas (
  empresa_id, codigo, descricao, tipo, natureza, dre_grupo, subgrupo, nivel,
  conta_pai_id, aceita_lancamento
) VALUES (
  1, '5.8', 'despesa:das', 'A', 'D', 'DESPESA_OPERACIONAL', 'IMPOSTOS', 2,
  (SELECT id FROM plano_contas WHERE empresa_id=1 AND codigo='5'), 1
);

-- 5.9 ISS
INSERT INTO plano_contas (
  empresa_id, codigo, descricao, tipo, natureza, dre_grupo, subgrupo, nivel,
  conta_pai_id, aceita_lancamento
) VALUES (
  1, '5.9', 'despesa:iss', 'A', 'D', 'DESPESA_OPERACIONAL', 'IMPOSTOS', 2,
  (SELECT id FROM plano_contas WHERE empresa_id=1 AND codigo='5'), 1
);

-- 5.10 Tarifas
INSERT INTO plano_contas (
  empresa_id, codigo, descricao, tipo, natureza, dre_grupo, subgrupo, nivel,
  conta_pai_id, aceita_lancamento
) VALUES (
  1, '5.10', 'despesa:tarifas', 'A', 'D', 'RESULTADO_FINANCEIRO', 'CAPITAL_TERCEIROS', 2,
  (SELECT id FROM plano_contas WHERE empresa_id=1 AND codigo='5'), 1
);

-- 5.11 Juros
INSERT INTO plano_contas (
  empresa_id, codigo, descricao, tipo, natureza, dre_grupo, subgrupo, nivel,
  conta_pai_id, aceita_lancamento
) VALUES (
  1, '5.11', 'despesa:juros', 'A', 'D', 'RESULTADO_FINANCEIRO', 'CAPITAL_TERCEIROS', 2,
  (SELECT id FROM plano_contas WHERE empresa_id=1 AND codigo='5'), 1
);

-- ====================================================================
-- FIM DO SCRIPT
-- ====================================================================
-- Verificacao: execute
-- SELECT codigo, descricao, tipo, natureza FROM plano_contas
-- WHERE empresa_id = 1 ORDER BY codigo;
-- Resultado esperado: 40 contas inseridas (incluindo contas sinteticas).