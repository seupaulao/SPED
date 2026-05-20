-- Script de inserção: Primeiro Plano de Contas
-- Modelo baseado em hledger para escritório contábil (médico PJ)
-- Estrutura: ativo:bank:conta_corrente, receita:servicos:medicos, etc.

-- Observação: Este script assume empresa_id = 1
-- Se precisar para outra empresa, substitua o valor de empresa_id

-- ====================================================================
-- CONTAS RAIZ (SINTÉTICAS - NÍVEL 1)
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

-- 3. PATRIMÔNIO LÍQUIDO
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
  1, '5', 'despesa', 'S', 'D', 2, NULL, 0
);

-- ====================================================================
-- SUBCONTAS DE ATIVO (NÍVEL 2)
-- ====================================================================

-- 1.1 BANK (grupo de contas bancárias)
INSERT INTO plano_contas (
  empresa_id, codigo, descricao, tipo, natureza, grupo, nivel, 
  conta_pai_id, aceita_lancamento
) VALUES (
  1, '1.1', 'ativo:banco', 'S', 'D', 'ATIVO', 2, 
  (SELECT id FROM plano_contas WHERE empresa_id=1 AND codigo='1'), 0
);

-- 1.1.1 Conta Corrente (analítica - aceita lançamento)
INSERT INTO plano_contas (
  empresa_id, codigo, descricao, tipo, natureza, grupo, nivel, 
  conta_pai_id, aceita_lancamento
) VALUES (
  1, '1.1.1', 'ativo:banco:conta_corrente', 'A', 'D', 'ATIVO', 3, 
  (SELECT id FROM plano_contas WHERE empresa_id=1 AND codigo='1.1'), 1
);

-- ====================================================================
-- SUBCONTAS DE PASSIVO (NÍVEL 2)
-- ====================================================================

-- 2.1 INSS a Pagar
INSERT INTO plano_contas (
  empresa_id, codigo, descricao, tipo, natureza, grupo, nivel, 
  conta_pai_id, aceita_lancamento
) VALUES (
  1, '2.1', 'passivo:inss_a_pagar', 'A', 'C', 'PASSIVO', 2, 
  (SELECT id FROM plano_contas WHERE empresa_id=1 AND codigo='2'), 1
);

-- 2.2 Pró-Labore a Pagar
INSERT INTO plano_contas (
  empresa_id, codigo, descricao, tipo, natureza, grupo, nivel, 
  conta_pai_id, aceita_lancamento
) VALUES (
  1, '2.2', 'passivo:prolabore_a_pagar', 'A', 'C', 'PASSIVO', 2, 
  (SELECT id FROM plano_contas WHERE empresa_id=1 AND codigo='2'), 1
);

-- 2.3 Impostos a Pagar
INSERT INTO plano_contas (
  empresa_id, codigo, descricao, tipo, natureza, grupo, nivel, 
  conta_pai_id, aceita_lancamento
) VALUES (
  1, '2.3', 'passivo:impostos_a_pagar', 'A', 'C', 'PASSIVO', 2, 
  (SELECT id FROM plano_contas WHERE empresa_id=1 AND codigo='2'), 1
);

-- ====================================================================
-- SUBCONTAS DE PATRIMÔNIO LÍQUIDO (NÍVEL 2)
-- ====================================================================

-- 3.1 Lucros
INSERT INTO plano_contas (
  empresa_id, codigo, descricao, tipo, natureza, grupo, nivel, 
  conta_pai_id, aceita_lancamento
) VALUES (
  1, '3.1', 'patrimonioliquido:lucros', 'A', 'C', 'PL', 2, 
  (SELECT id FROM plano_contas WHERE empresa_id=1 AND codigo='3'), 1
);

-- ====================================================================
-- SUBCONTAS DE RECEITA (NÍVEL 2)
-- ====================================================================

-- 4.1 Serviços (grupo sintético)
INSERT INTO plano_contas (
  empresa_id, codigo, descricao, tipo, natureza, dre_grupo, nivel, 
  conta_pai_id, aceita_lancamento
) VALUES (
  1, '4.1', 'receita:servicos', 'S', 'C', 'RECEITA_BRUTA', 2, 
  (SELECT id FROM plano_contas WHERE empresa_id=1 AND codigo='4'), 0
);

-- 4.1.1 Serviços Médicos (analítica - aceita lançamento)
INSERT INTO plano_contas (
  empresa_id, codigo, descricao, tipo, natureza, dre_grupo, subgrupo, nivel, 
  conta_pai_id, aceita_lancamento
) VALUES (
  1, '4.1.1', 'receita:servicos:medicos', 'A', 'C', 'RECEITA_BRUTA', 'RECEITAS', 3, 
  (SELECT id FROM plano_contas WHERE empresa_id=1 AND codigo='4.1'), 1
);

-- ====================================================================
-- SUBCONTAS DE DESPESA (NÍVEL 2)
-- ====================================================================

-- 5.1 Pró-Labore (analítica)
INSERT INTO plano_contas (
  empresa_id, codigo, descricao, tipo, natureza, dre_grupo, subgrupo, nivel, 
  conta_pai_id, aceita_lancamento
) VALUES (
  1, '5.1', 'despesa:prolabore', 'A', 'D', 'DESPESA_OPERACIONAL', 'PESSOAL', 2, 
  (SELECT id FROM plano_contas WHERE empresa_id=1 AND codigo='5'), 1
);

-- 5.2 INSS (analítica)
INSERT INTO plano_contas (
  empresa_id, codigo, descricao, tipo, natureza, dre_grupo, subgrupo, nivel, 
  conta_pai_id, aceita_lancamento
) VALUES (
  1, '5.2', 'despesa:inss', 'A', 'D', 'DESPESA_OPERACIONAL', 'PESSOAL', 2, 
  (SELECT id FROM plano_contas WHERE empresa_id=1 AND codigo='5'), 1
);

-- 5.3 Simples Nacional (analítica)
INSERT INTO plano_contas (
  empresa_id, codigo, descricao, tipo, natureza, dre_grupo, subgrupo, nivel, 
  conta_pai_id, aceita_lancamento
) VALUES (
  1, '5.3', 'despesa:simples_nacional', 'A', 'D', 'DESPESA_OPERACIONAL', 'IMPOSTOS', 2, 
  (SELECT id FROM plano_contas WHERE empresa_id=1 AND codigo='5'), 1
);

-- ====================================================================
-- FIM DO SCRIPT
-- ====================================================================
-- Verificação: execute "SELECT * FROM plano_contas WHERE empresa_id=1 ORDER BY codigo;" 
-- para confirmar se todas as 13 contas foram inseridas com sucesso.
