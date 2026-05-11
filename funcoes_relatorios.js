async function balancete(db, dataInicio, dataFim) {
  const rows = await db.all(`
    SELECT 
      c.id,
      c.codigo,
      c.descricao,
      c.natureza,

      SUM(CASE WHEN li.tipo='D' THEN li.valor ELSE 0 END) AS debitos,
      SUM(CASE WHEN li.tipo='C' THEN li.valor ELSE 0 END) AS creditos

    FROM plano_contas c
    LEFT JOIN lancamento_item li ON li.conta_id = c.id
    LEFT JOIN lancamento l ON l.id = li.lancamento_id

    WHERE l.data BETWEEN ? AND ?
    GROUP BY c.id
    ORDER BY c.codigo
  `, [dataInicio, dataFim]);

  return rows.map(r => {
    const deb = toNumber(r.debitos);
    const cred = toNumber(r.creditos);

    const saldo = r.natureza === 'D'
      ? deb - cred
      : cred - deb;

    return {
      ...r,
      saldo
    };
  });
}


async function balancoPatrimonial(db, dataInicio, dataFim) {
  const dados = await balancete(db, dataInicio, dataFim);

  const ativo = [];
  const passivo = [];
  const pl = [];

  for (const c of dados) {
    if (c.saldo === 0) continue;

    if (c.grupo === 'ATIVO') ativo.push(c);
    if (c.grupo === 'PASSIVO') passivo.push(c);
    if (c.grupo === 'PL') pl.push(c);
  }

  return {
    ativo,
    passivo,
    patrimonio_liquido: pl,
    total_ativo: ativo.reduce((s, i) => s + i.saldo, 0),
    total_passivo_pl: [...passivo, ...pl].reduce((s, i) => s + i.saldo, 0)
  };
}


async function dre(db, dataInicio, dataFim) {
  const dados = await balancete(db, dataInicio, dataFim);

  const grupos = {};

  for (const c of dados) {
    if (!c.dre_grupo) continue;

    if (!grupos[c.dre_grupo]) grupos[c.dre_grupo] = 0;

    grupos[c.dre_grupo] += c.saldo;
  }

  const receita = toNumber(grupos.RECEITA_BRUTA);
  const custo = toNumber(grupos.CUSTO);
  const despesa = toNumber(grupos.DESPESA_OPERACIONAL);
  const financeiro = toNumber(grupos.RESULTADO_FINANCEIRO);

  const resultado = receita - custo - despesa + financeiro;

  return {
    receita,
    custo,
    despesa,
    financeiro,
    resultado
  };
}

async function dva(db, dataInicio, dataFim) {
  const dados = await balancete(db, dataInicio, dataFim);

  let receitas = 0;
  let insumos = 0;
  let pessoal = 0;
  let impostos = 0;
  let capitalTerceiros = 0;

  for (const c of dados) {
    if (!c.subgrupo) continue;

    switch (c.subgrupo) {
      case 'RECEITAS':
        receitas += c.saldo;
        break;
      case 'INSUMOS':
        insumos += c.saldo;
        break;
      case 'PESSOAL':
        pessoal += c.saldo;
        break;
      case 'IMPOSTOS':
        impostos += c.saldo;
        break;
      case 'CAPITAL_TERCEIROS':
        capitalTerceiros += c.saldo;
        break;
    }
  }

  const valorAdicionado = receitas - insumos;

  return {
    receitas,
    insumos,
    valor_adicionado: valorAdicionado,
    distribuicao: {
      pessoal,
      impostos,
      capital_terceiros: capitalTerceiros
    }
  };
}

async function dfc(db, dataInicio, dataFim) {
  const dados = await balancete(db, dataInicio, dataFim);

  let operacional = 0;
  let investimento = 0;
  let financiamento = 0;

  for (const c of dados) {
    switch (c.fluxo_caixa_tipo) {
      case 'OPERACIONAL':
        operacional += c.saldo;
        break;
      case 'INVESTIMENTO':
        investimento += c.saldo;
        break;
      case 'FINANCIAMENTO':
        financiamento += c.saldo;
        break;
    }
  }

  return {
    operacional,
    investimento,
    financiamento,
    variacao_caixa: operacional + investimento + financiamento
  };
}
