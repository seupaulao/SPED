
import sqlite3
from utils import *


def menu_nota_fiscal(conn: sqlite3.Connection) -> None:
    empresa = ask_empresa(conn)
    print("\n------\n")
    tomador = ask_tomador(conn)
    if not empresa or not tomador:
        return
    while True:
        print("\n[a] Criar Nota Fiscal")
        print("[b] Visualizar Notas Fiscais")
        print("[c] Excluir Nota Fiscal")
        print("[q] Voltar")
        choice = input("\nEscolha: ").strip().lower()
        if choice == "a":
            criar_nota_fiscal(conn, empresa, tomador)
        elif choice == "b":
            visualizar_notas_fiscais(conn, empresa)
        elif choice == "c":
            excluir_nota_fiscal(conn, empresa)
        elif choice == "q":
            return
        else:
            pause("Opção inválida. Clique ENTER para tentar novamente.")

def criar_nota_fiscal(conn: sqlite3.Connection, empresa: dict, tomador: dict) -> None:
    print("\nCriar Nota Fiscal")
    print("-" * 20)
    data_emissao = input("Data de Emissão (DD/MM/AAAA): ").strip()
    try:
        data_emissao = normalize_date(data_emissao)
    except ValueError as e:
        pause(str(e))
        return
    valor_total = input("Valor Total: ").strip()
    try:
        valor_total = parse_decimal(valor_total)
    except ValueError as e:
        pause(str(e))
        return
    numero = input("Número: ").strip()
    codigo = input("Código: ").strip()
    chave_acesso = input("Chave de Acesso: ").strip()
    situacao = input("Situação: ").strip()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO notas_fiscais (empresa_id, tomador_id, data_emissao, valor_total, numero, codigo, chave_acesso, situacao) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (empresa["id"], tomador["id"], data_emissao, valor_total, numero, codigo, chave_acesso, situacao),
    )
    conn.commit()
    pause("Nota Fiscal criada com sucesso.")

def visualizar_notas_fiscais(conn: sqlite3.Connection, empresa: dict) -> None:
    print("\nNotas Fiscais")
    print("-" * 20)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, numero, data_emissao, valor_total, situacao FROM notas_fiscais WHERE empresa_id = ? ORDER BY data_emissao DESC",
        (empresa["id"],),
    )
    rows = cursor.fetchall()
    if not rows:
        print("Nenhuma Nota Fiscal encontrada.")
        pause()
        return
    print(f"{'ID':<5} {'Número':<10} {'Data de Emissão':<15} {'Valor Total':>15} {'Situação':<10}")
    print("-" * 60)
    for row in rows:
        id, numero, data_emissao, valor_total, situacao = row
        data_emissao = display_date(data_emissao)
        valor_total = format_currency(valor_total)
        print(f"{id:<5} {numero:<10} {data_emissao:<15} {valor_total:>15} {situacao:<10}")
    pause()

def excluir_nota_fiscal(conn: sqlite3.Connection, empresa: dict) -> None:
    print("\nExcluir Nota Fiscal")
    print("-" * 20)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, numero, data_emissao FROM notas_fiscais WHERE empresa_id = ? ORDER BY data_emissao DESC",
        (empresa["id"],),
    )
    rows = cursor.fetchall()
    if not rows:
        print("Nenhuma Nota Fiscal encontrada.")
        pause()
        return
    print(f"{'ID':<5} {'Número':<10} {'Data de Emissão':<15}")
    print("-" * 35)
    for row in rows:
        id, numero, data_emissao = row
        data_emissao = display_date(data_emissao)
        print(f"{id:<5} {numero:<10} {data_emissao:<15}")
    try:
        nota_id = int(input("\nDigite o ID da Nota Fiscal a excluir: ").strip())
    except ValueError:
        pause("ID inválido. Clique ENTER para tentar novamente.")
        return
    cursor.execute("DELETE FROM notas_fiscais WHERE id = ? AND empresa_id = ?", (nota_id, empresa["id"]))
    if cursor.rowcount == 0:
        pause("Nota Fiscal não encontrada ou não pertence à empresa selecionada. Clique ENTER para tentar novamente.")
    else:
        conn.commit()
        pause("Nota Fiscal excluída com sucesso.")  