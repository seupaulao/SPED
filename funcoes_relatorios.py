"""
Módulo de funções de relatórios (portado de funcoes_relatorios.js).
Implementa: balancete, balanco_patrimonial, dre, dva, dfc.
Assume conexão sqlite3 (DB API). Retorna estruturas em dicionários/listas.
"""

from typing import List, Dict, Any
import sqlite3

__all__ = [
    "balancete",
    "balanco_patrimonial",
    "dre",
    "dva",
    "dfc",
    "to_number",
]


def to_number(value: Any) -> float:
    """Converte valores nulos/strings para float com fallback 0."""
    if value is None:
        return 0.0
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0


def balancete(db: sqlite3.Connection, data_inicio: str, data_fim: str) -> List[Dict[str, Any]]:
    """
    Retorna lista de contas com debitos, creditos e saldo entre datas.
    data_inicio and data_fim devem ser strings compatíveis com o formato da coluna l.data.
    """
    sql = """
    SELECT 
      c.id,
      c.codigo,
      c.descricao,
      c.natureza,
      c.grupo,
      c.dre_grupo,
      c.subgrupo,
      c.fluxo_caixa_tipo,

      SUM(CASE WHEN li.tipo='D' THEN li.valor ELSE 0 END) AS debitos,
      SUM(CASE WHEN li.tipo='C' THEN li.valor ELSE 0 END) AS creditos

    FROM plano_contas c
    LEFT JOIN lancamento_item li ON li.conta_id = c.id
    LEFT JOIN lancamento l ON l.id = li.lancamento_id

    WHERE l.data BETWEEN ? AND ?
    GROUP BY c.id
    ORDER BY c.codigo
    """

    cur = db.cursor()
    cur.execute(sql, (data_inicio, data_fim))
    rows = cur.fetchall()

    # Ensure rows are accessible by name if using row_factory; otherwise map manually
    cols = [d[0] for d in cur.description]

    result = []
    for row in rows:
        r = dict(zip(cols, row))
        deb = to_number(r.get("debitos"))
        cred = to_number(r.get("creditos"))

        natureza = r.get("natureza")
        if natureza == 'D':
            saldo = deb - cred
        else:
            saldo = cred - deb

        r["debitos"] = deb
        r["creditos"] = cred
        r["saldo"] = saldo

        result.append(r)

    return result


def balanco_patrimonial(db: sqlite3.Connection, data_inicio: str, data_fim: str) -> Dict[str, Any]:
    dados = balancete(db, data_inicio, data_fim)

    ativo = []
    passivo = []
    pl = []

    for c in dados:
        if c.get("saldo") == 0:
            continue

        grupo = c.get("grupo")
        if grupo == 'ATIVO':
            ativo.append(c)
        elif grupo == 'PASSIVO':
            passivo.append(c)
        elif grupo == 'PL':
            pl.append(c)

    total_ativo = sum([to_number(i.get("saldo")) for i in ativo])
    total_passivo_pl = sum([to_number(i.get("saldo")) for i in (passivo + pl)])

    return {
        "ativo": ativo,
        "passivo": passivo,
        "patrimonio_liquido": pl,
        "total_ativo": total_ativo,
        "total_passivo_pl": total_passivo_pl,
    }


def dre(db: sqlite3.Connection, data_inicio: str, data_fim: str) -> Dict[str, float]:
    dados = balancete(db, data_inicio, data_fim)

    grupos = {}
    for c in dados:
        chave = c.get("dre_grupo")
        if not chave:
            continue
        grupos[chave] = grupos.get(chave, 0.0) + to_number(c.get("saldo"))

    receita = to_number(grupos.get("RECEITA_BRUTA"))
    custo = to_number(grupos.get("CUSTO"))
    despesa = to_number(grupos.get("DESPESA_OPERACIONAL"))
    financeiro = to_number(grupos.get("RESULTADO_FINANCEIRO"))

    resultado = receita - custo - despesa + financeiro

    return {
        "receita": receita,
        "custo": custo,
        "despesa": despesa,
        "financeiro": financeiro,
        "resultado": resultado,
    }


def dva(db: sqlite3.Connection, data_inicio: str, data_fim: str) -> Dict[str, Any]:
    dados = balancete(db, data_inicio, data_fim)

    receitas = 0.0
    insumos = 0.0
    pessoal = 0.0
    impostos = 0.0
    capital_terceiros = 0.0

    for c in dados:
        sub = c.get("subgrupo")
        if not sub:
            continue
        if sub == 'RECEITAS':
            receitas += to_number(c.get("saldo"))
        elif sub == 'INSUMOS':
            insumos += to_number(c.get("saldo"))
        elif sub == 'PESSOAL':
            pessoal += to_number(c.get("saldo"))
        elif sub == 'IMPOSTOS':
            impostos += to_number(c.get("saldo"))
        elif sub == 'CAPITAL_TERCEIROS':
            capital_terceiros += to_number(c.get("saldo"))

    valor_adicionado = receitas - insumos

    return {
        "receitas": receitas,
        "insumos": insumos,
        "valor_adicionado": valor_adicionado,
        "distribuicao": {
            "pessoal": pessoal,
            "impostos": impostos,
            "capital_terceiros": capital_terceiros,
        },
    }


def dfc(db: sqlite3.Connection, data_inicio: str, data_fim: str) -> Dict[str, float]:
    dados = balancete(db, data_inicio, data_fim)

    operacional = 0.0
    investimento = 0.0
    financiamento = 0.0

    for c in dados:
        tipo = c.get("fluxo_caixa_tipo")
        if tipo == 'OPERACIONAL':
            operacional += to_number(c.get("saldo"))
        elif tipo == 'INVESTIMENTO':
            investimento += to_number(c.get("saldo"))
        elif tipo == 'FINANCIAMENTO':
            financiamento += to_number(c.get("saldo"))

    variacao_caixa = operacional + investimento + financiamento

    return {
        "operacional": operacional,
        "investimento": investimento,
        "financiamento": financiamento,
        "variacao_caixa": variacao_caixa,
    }
