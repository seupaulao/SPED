"""
Valida consultas usando o arquivo contabilidade.db na mesma pasta.
Imprime resumos de cada relatório. Execute localmente quando desejar.
"""

import sqlite3
import sys
from pathlib import Path
from pprint import pprint

import funcoes_relatorios as frp


def main():
    db_path = Path(__file__).parent / 'contabilidade.db'
    if not db_path.exists():
        print(f"Arquivo de banco não encontrado: {db_path}")
        sys.exit(2)

    conn = sqlite3.connect(str(db_path))

    try:
        cur = conn.cursor()
        cur.execute("SELECT MIN(data), MAX(data) FROM lancamento")
        row = cur.fetchone()
        data_inicio = row[0] if row and row[0] else '1900-01-01'
        data_fim = row[1] if row and row[1] else '2100-12-31'

        print(f"Usando intervalo: {data_inicio} -> {data_fim}")

        bal = frp.balancete(conn, data_inicio, data_fim)
        print(f"Balancete: {len(bal)} contas (mostrando até 10)")
        pprint(bal[:10])

        bp = frp.balanco_patrimonial(conn, data_inicio, data_fim)
        print("Balanco patrimonial resumo:")
        pprint({
            'total_ativo': bp.get('total_ativo'),
            'total_passivo_pl': bp.get('total_passivo_pl'),
            'ativas_qtd': len(bp.get('ativo', [])),
            'passivo_qtd': len(bp.get('passivo', [])),
            'pl_qtd': len(bp.get('patrimonio_liquido', [])),
        })

        dre = frp.dre(conn, data_inicio, data_fim)
        print("DRE resumo:")
        pprint(dre)

        dva = frp.dva(conn, data_inicio, data_fim)
        print("DVA resumo:")
        pprint(dva)

        dfc = frp.dfc(conn, data_inicio, data_fim)
        print("DFC resumo:")
        pprint(dfc)

    except Exception as e:
        print("Erro ao validar banco:", e)
        sys.exit(1)
    finally:
        conn.close()


if __name__ == '__main__':
    main()
