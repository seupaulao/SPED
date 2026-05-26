from __future__ import annotations

import sqlite3
from utils import *
from empresa import *
from contas import *
from lancamento import *

import funcoes_relatorios as relatorios


#APP_TITLE = "PJLA Contabilidade OFFLINE"
#BASE_DIR = Path(__file__).resolve().parent.parent
#DB_PATH = BASE_DIR / "contabilidade_simples.db"

#SCHEMA_PATH = BASE_DIR / "banco_sqlite3.sql"


def menu_livro_diario(conn: sqlite3.Connection) -> None:
    empresa = ask_empresa(conn)
    if not empresa:
        return
    while True:
        print("\n[a] Criar Lançamento")
        print("[b] Corrigir Lançamento")
        print("[c] Apagar Lançamento")
        print("[d] Visualizar todos os Lançamentos")
        print("[e] Lançamento Estorno")
        print("[f] Lançamento Ajuste")
        print("[q] Voltar ao menu principal")
        choice = input("\nEscolha: ").strip().lower()
        if choice == "a":
            criar_lancamento(conn, empresa)
        elif choice == "b":
            corrigir_lancamento(conn, empresa)
        elif choice == "c":
            apagar_lancamento(conn, empresa)
        elif choice == "d":
            visualizar_lancamentos(conn, empresa)
        elif choice == "e":
            criar_lancamento_estorno(conn, empresa)
        elif choice == "f":
            criar_lancamento_ajuste(conn, empresa)
        elif choice == "q":
            return
        else:
            pause("Opção inválida. Clique ENTER para tentar novamente.")


def menu_relatorios(conn: sqlite3.Connection) -> None:
    empresa = ask_empresa(conn)
    if not empresa:
        return
    while True:
        print("\n[b] Balancete")
        print("[c] Balanço Patrimonial")
        print("[d] DRE")
        print("[e] DVA")
        print("[q] Voltar")
        choice = input("\nEscolha: ").strip().lower()
        if choice == "q":
            return
        if choice not in {"b", "c", "d", "e"}:
            pause("Opção inválida. Clique ENTER para tentar novamente.")
            continue
        period = ask_period()
        if not period:
            continue
        data_inicio, data_fim = period
        if choice == "b":
            rows = relatorios.balancete(conn, data_inicio, data_fim, empresa_id=empresa["id"])
            print_rows("Balancete", rows)
            pause()
        elif choice == "c":
            result = relatorios.balanco_patrimonial(conn, data_inicio, data_fim, empresa_id=empresa["id"])
            print_key_values("Balanço Patrimonial", result)
            pause()
        elif choice == "d":
            result = relatorios.dre(conn, data_inicio, data_fim, empresa_id=empresa["id"])
            print_key_values("DRE", result)
            pause()
        elif choice == "e":
            result = relatorios.dva(conn, data_inicio, data_fim, empresa_id=empresa["id"])
            print_key_values("DVA", result)
            pause()


def menu_ecd(conn: sqlite3.Connection) -> None:
    empresa = ask_empresa(conn)
    if not empresa:
        return
    pause("Geração ECD pendente de detalhamento na especificação.")


def main() -> None:
    conn = connect_db()
    try:
        while True:
            print_header()
            print("[a] Livro Diario")
            print("[b] Relatórios")
            print("[c] Cadastro Empresa")
            print("[d] Gerar ECD")
            print("[e] Plano de Contas")
            print("[q] Sair")

            choice = input("\nEscolha: ").strip().lower()
            if choice == "a":
                menu_livro_diario(conn)
            elif choice == "b":
                menu_relatorios(conn)
            elif choice == "c":
                menu_cadastro_empresa(conn)
            elif choice == "d":
                menu_ecd(conn)
            elif choice == "e":
                menu_plano_contas(conn)    
            elif choice == "q":
                return
            else:
                pause("Opção inválida. Clique ENTER para tentar novamente.")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
