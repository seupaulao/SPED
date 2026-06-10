from __future__ import annotations

import sqlite3
from utils import *
from empresa import *
from contas import *
from lancamento import *
from nota_fiscal import *
from tomador import *
from trava_contabil import *
from mapa import *

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
    if is_empresa_table_empty(conn):
        print("Nenhuma empresa cadastrada. Por favor, cadastre uma empresa para continuar.")
        menu_cadastro_empresa(conn)
    if not trava_contabil_existe(conn, datetime.today().month, datetime.today().year):
        criar_trava_contabil_automatica_mensal(conn)
        print("Trava Contábil do mês criada automaticamente.")
    try:
        while True:
            print_header()
            print("[a] Livro Diario")
            print("[b] Relatórios")
            print("[c] Cadastro Empresa")
            print("[d] Gerar ECD")
            print("[e] Plano de Contas")
            print("[f] Nota Fiscal")
            print("[g] Tomadores")
            print("[i] Avaliação Imposto")
            print("[h] Realizar Trava Contábil do Exercício")
            print("[j] Gerar Mapa de Demonstrações Contábeis")
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
            elif choice == "f":
                menu_nota_fiscal(conn)
            elif choice == "g":
                menu_tomador(conn)
            elif choice == "i":
                menu_avaliacao_imposto() 
            elif choice == "h":
                menu_trava_contabil(conn)
            elif choice == "q":
                return
            elif choice == "j":
                menu_mapa_demontracoes(conn)
            else:
                pause("Opção inválida. Clique ENTER para tentar novamente.")
    finally:
        conn.close()


def menu_avaliacao_imposto():
    receita=float(input("\nReceita: "))
    ppro=float(input("\n% Prolabore [Inteiro]: "))
    perpro = ppro / 100
    prolabore = receita * perpro
    iss = receita * 0.03
    inss = prolabore * 0.11
    anexo = 5
    if perpro >= 0.28:
       anexo = 3
    peranexo = 0.155
    if anexo == 3:
       peranexo = 0.06
    DAS=receita * peranexo
    print("Prolabore   : {:.2f} a {:.2f}%".format(prolabore, ppro))
    print("ISS         : {:.2f}".format(iss))
    liq = receita - iss
    print("NF          : {:.2f}".format(liq)) 
    print("INSS        : {:.2f}".format(inss))
    ianexo = peranexo * 100
    print("DAS         : {:.2f}, Anexo: {} - {:.2f}%".format(DAS, anexo, ianexo))
    total = inss + DAS
    print("Total Imp   : {:.2f}".format(total))
    saldo = liq - total
    print("Saldo       : {:.2f}".format(saldo))   

if __name__ == "__main__":
    main()
