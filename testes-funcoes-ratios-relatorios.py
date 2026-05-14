"""
Testes rápidos para finantial_ratios.py e funcoes_relatorios.py.
Executa verificações em memória (sqlite) para validar comportamento básico.
"""

import sqlite3
import sys
from pprint import pprint

import finantial_ratios as fr
import funcoes_relatorios as frp


def test_ratios():
    print("Testando funções de indicadores...")
    assert abs(fr.current_ratio(150, 100) - 1.5) < 1e-9
    assert abs(fr.gross_margin(1000, 600) - 0.4) < 1e-9
    assert abs(fr.roa(50, 1000) - 0.05) < 1e-9
    print("- Ratios básicos OK")


def setup_db():
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()

    # Cria esquema mínimo para os relatórios
    cur.executescript("""
    CREATE TABLE plano_contas (
        id INTEGER PRIMARY KEY,
        codigo TEXT,
        descricao TEXT,
        natureza TEXT,
        grupo TEXT,
        dre_grupo TEXT,
        subgrupo TEXT,
        fluxo_caixa_tipo TEXT
    );

    CREATE TABLE lancamento (
        id INTEGER PRIMARY KEY,
        data TEXT
    );

    CREATE TABLE lancamento_item (
        id INTEGER PRIMARY KEY,
        lancamento_id INTEGER,
        conta_id INTEGER,
        tipo TEXT,
        valor REAL
    );
    """)

    # Inserir contas de exemplo
    contas = [
        (1, '1.1.1', 'Caixa', 'D', 'ATIVO', None, None, None),
        (2, '2.1.1', 'Fornecedores', 'C', 'PASSIVO', None, None, None),
        (3, '3.1.1', 'Patrimonio', 'C', 'PL', None, None, None),
        (4, '4.1.1', 'Receita', 'C', None, 'RECEITA_BRUTA', 'RECEITAS', None),
        (5, '5.1.1', 'Custo', 'D', None, 'CUSTO', 'INSUMOS', None),
    ]

    for t in contas:
        # Note: ordem dos campos: id,codigo,descricao,natureza,grupo,dre_grupo,subgrupo,fluxo_caixa_tipo
        cur.execute(
            "INSERT INTO plano_contas (id,codigo,descricao,natureza,grupo,dre_grupo,subgrupo,fluxo_caixa_tipo) VALUES (?,?,?,?,?,?,?,?)",
            t,
        )

    # Inserir um lançamento e itens
    cur.execute("INSERT INTO lancamento (id,data) VALUES (1,'2022-01-15')")

    itens = [
        (1, 1, 1, 'D', 1000.0),  # debita caixa
        (2, 1, 4, 'C', 1000.0),  # credita receita
        (3, 1, 5, 'D', 600.0),   # debita custo
        (4, 1, 2, 'C', 400.0),   # credita fornecedores
    ]

    for it in itens:
        cur.execute("INSERT INTO lancamento_item (id,lancamento_id,conta_id,tipo,valor) VALUES (?,?,?,?,?)", it)

    conn.commit()
    return conn


def test_reports():
    print("Testando funções de relatórios em DB em memória...")
    conn = setup_db()

    bal = frp.balancete(conn, '2022-01-01', '2022-12-31')
    print("- Balancete: linhas =", len(bal))
    assert len(bal) >= 1

    bp = frp.balanco_patrimonial(conn, '2022-01-01', '2022-12-31')
    print("- Balanco patrimonial resumo:")
    pprint({k: (len(v) if isinstance(v, list) else v) for k, v in bp.items()})

    dre = frp.dre(conn, '2022-01-01', '2022-12-31')
    print("- DRE:")
    pprint(dre)

    dva = frp.dva(conn, '2022-01-01', '2022-12-31')
    print("- DVA:")
    pprint(dva)

    dfc = frp.dfc(conn, '2022-01-01', '2022-12-31')
    print("- DFC:")
    pprint(dfc)

    print("Todos os testes em memória passaram.")


if __name__ == '__main__':
    try:
        test_ratios()
        test_reports()
    except AssertionError as e:
        print("Teste falhou:", e)
        sys.exit(2)
    except Exception as e:
        print("Erro durante testes:", e)
        sys.exit(1)
    else:
        print("SUCESSO: todos os testes passaram")
