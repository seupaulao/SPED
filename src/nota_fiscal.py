
import sqlite3
from utils import *
from rich.console import Console
from rich.table import Table
from rich import box

_console = Console()


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
    referencia = input("Referência: ").strip()
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
        "INSERT INTO nota_fiscal (empresa_id, tomador_id, referencia, data_emissao, valor_total, numero, codigo, chave_acesso, situacao) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (empresa["id"], tomador["id"], referencia, data_emissao, valor_total, numero, codigo, chave_acesso, situacao),
    )
    conn.commit()
    pause("Nota Fiscal criada com sucesso.")

def visualizar_notas_fiscais(conn: sqlite3.Connection, empresa: dict) -> None:
    print("\nNotas Fiscais")
    print("-" * 20)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, numero, data_emissao, valor_total, situacao FROM nota_fiscal WHERE empresa_id = ? ORDER BY data_emissao DESC",
        (empresa["id"],),
    )
    rows = cursor.fetchall()
    if not rows:
        print("Nenhuma Nota Fiscal encontrada.")
        pause()
        return

    table = Table(box=box.SIMPLE_HEAVY, show_lines=False)
    table.add_column("ID", justify="right", no_wrap=True)
    table.add_column("Número", no_wrap=True)
    table.add_column("Data de Emissão", no_wrap=True)
    table.add_column("Valor Total", justify="right", no_wrap=True)
    table.add_column("Situação", no_wrap=True)

    for id, numero, data_emissao, valor_total, situacao in rows:
        table.add_row(
            str(id),
            str(numero) if numero is not None else "",
            display_date(data_emissao),
            format_currency(valor_total),
            str(situacao) if situacao is not None else "",
        )

    _console.print(table)
    pause()

def excluir_nota_fiscal(conn: sqlite3.Connection, empresa: dict) -> None:
    print("\nExcluir Nota Fiscal")
    print("-" * 20)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, numero, data_emissao FROM nota_fiscal WHERE empresa_id = ? ORDER BY data_emissao DESC",
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
    cursor.execute("DELETE FROM nota_fiscal WHERE id = ? AND empresa_id = ?", (nota_id, empresa["id"]))
    if cursor.rowcount == 0:
        pause("Nota Fiscal não encontrada ou não pertence à empresa selecionada. Clique ENTER para tentar novamente.")
    else:
        conn.commit()
        pause("Nota Fiscal excluída com sucesso.")  