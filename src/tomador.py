import sqlite3
from utils import *
from rich.console import Console
from rich.table import Table
from rich import box

_console = Console()

EMPRESA_FIELDS = [
    ("cnpj", "CNPJ", True, "text"),
    ("nome", "NOME", True, "text"),
    ("uf", "UF", False, "text"),
    ("municipio", "MUNICIPIO", False, "text"),
    ("data_inicio", "DATA DE INICIO", False, "date"),
    ("data_fim", "DATA DE FIM", False, "date"),
]

def menu_tomador(conn: sqlite3.Connection) -> None:
    while True:
        print("\n[a] Inserir Tomador")
        print("[b] Excluir Tomador")
        print("[d] Visualizar Tomador")
        print("[c] Listar Tomadores")
        print("[q] Voltar")
        choice = input("\nEscolha: ").strip().lower()
        if choice == "a":
            inserir_tomador(conn)
        elif choice == "b":
            excluir_tomador(conn)
        elif choice == "d":
            visualizar_tomadores(conn)
        elif choice == "c":
            listar_tomadores(conn)
        elif choice == "q":
            return
        else:
            pause("Opção inválida. Clique ENTER para tentar novamente.")

def inserir_tomador(conn: sqlite3.Connection) -> None:
    print("\nInserir Tomador")
    print("-" * 20)
    cnpj = input("CNPJ: ").strip()
    nome = input("Nome: ").strip()
    uf = input("UF: ").strip()
    municipio = input("Município: ").strip()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tomador (cnpj, nome, uf, municipio) VALUES (?, ?, ?, ?)",
        (cnpj, nome, uf, municipio),
    )
    conn.commit()
    pause("Tomador inserido com sucesso.")

def excluir_tomador(conn: sqlite3.Connection) -> None:
    print("\nExcluir Tomador")
    print("-" * 20)
    cnpj = input("CNPJ do Tomador a excluir: ").strip()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tomador WHERE cnpj = ?", (cnpj,))
    if cursor.rowcount == 0:
        pause("Tomador não encontrado.")
    else:
        conn.commit()
        pause("Tomador excluído com sucesso.")

def visualizar_tomadores(conn: sqlite3.Connection) -> None:
    print("\nTomadores")
    print("-" * 20)
    cursor = conn.cursor()
    cursor.execute("SELECT cnpj, nome, uf, municipio FROM tomador ORDER BY nome")
    rows = cursor.fetchall()
    if not rows:
        print("Nenhum tomador encontrado.")
        pause()
        return

    table = Table(box=box.SIMPLE_HEAVY, show_lines=False)
    table.add_column("CNPJ", no_wrap=True)
    table.add_column("NOME")
    table.add_column("UF", justify="center", no_wrap=True)
    table.add_column("MUNICÍPIO")

    for cnpj, nome, uf, municipio in rows:
        table.add_row(cnpj or "", nome or "", uf or "", municipio or "")

    _console.print(table)
    pause()

def listar_tomadores(conn: sqlite3.Connection) -> None:
    print("\nLista de Tomadores")
    print("-" * 20)
    cursor = conn.cursor()
    cursor.execute("SELECT cnpj, nome, uf, municipio FROM tomador ORDER BY nome")
    rows = cursor.fetchall()
    if not rows:
        print("Nenhum tomador encontrado.")
        pause()
        return

    table = Table(box=box.SIMPLE_HEAVY, show_lines=False)
    table.add_column("CNPJ", no_wrap=True)
    table.add_column("NOME")
    table.add_column("UF", justify="center", no_wrap=True)
    table.add_column("MUNICÍPIO")

    for cnpj, nome, uf, municipio in rows:
        table.add_row(cnpj or "", nome or "", uf or "", municipio or "")

    _console.print(table)
    pause()