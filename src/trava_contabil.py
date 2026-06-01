
import sqlite3
from utils import *

def menu_trava_contabil(conn: sqlite3.Connection) -> None:
    empresa = ask_empresa(conn)
    if not empresa:
        return
    while True:
        print("\n[a] Criar Trava Contábil")
        print("[b] Visualizar Travas Contábeis")
        print("[c] Fechar Trava Contábil")
        print("[d] Abrir Trava Contábil")
        print("[q] Voltar")
        choice = input("\nEscolha: ").strip().lower()
        if choice == "a":
            criar_trava_contabil(conn, empresa)
        elif choice == "b":
            visualizar_travas_contabeis(conn, empresa)
        elif choice == "c":
            fechar_trava_contabil(conn, empresa)
        elif choice == "d":
            abrir_trava_contabil(conn, empresa)
        elif choice == "q":
            return
        else:
            pause("Opção inválida. Clique ENTER para tentar novamente.")

def trava_contabil_existe(conn: sqlite3.Connection, mes: int, ano: int) -> bool:
    cursor = conn.cursor()
    cursor.execute(
        "SELECT COUNT(*) FROM trava_contabil WHERE mes = ? AND ano = ?",
        (mes, ano),
    )
    count = cursor.fetchone()[0]
    return count > 0

def criar_trava_contabil_automatica_mensal(conn: sqlite3.Connection) -> None:
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM empresa")
    empresas = cursor.fetchall()
    if not empresas:
        return
    today = datetime.today()
    mes = today.month
    ano = today.year
    if trava_contabil_existe(conn, mes, ano):
        return
    for (empresa_id,) in empresas:
        cursor.execute(
            "INSERT INTO trava_contabil (empresa_id, ano, mes, is_closed) VALUES (?, ?, ?, 0)",
            (empresa_id, ano, mes),
        )
    conn.commit()

def criar_trava_contabil(conn: sqlite3.Connection, empresa: dict) -> None:
    print("\nCriar Trava Contábil")
    print("-" * 20)
    mes = input("Mês: ").strip()
    ano = input("Ano: ").strip()

    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO trava_contabil (empresa_id, ano, mes, is_closed) VALUES (?, ?, ?, 0)",
        (empresa["id"], ano, mes),
    )
    conn.commit()
    pause("Trava Contábil criada com sucesso.")

def get_situacao_trava_contabil(conn, ano, mes, empresa_id) -> str:
    cursor = conn.cursor()
    cursor.execute(
        "SELECT is_closed FROM trava_contabil WHERE empresa_id = ? AND ano = ? AND mes = ?",
        (empresa_id, ano, mes),
    )
    row = cursor.fetchone()
    if row is None:
        return "Não encontrada"
    is_closed = row[0]
    return "Fechada" if is_closed else "Aberta"

def visualizar_travas_contabeis(conn: sqlite3.Connection, empresa: dict) -> None:
    print("\nTravas Contábeis")
    print("-" * 20)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT mes, ano, is_closed FROM trava_contabil WHERE empresa_id = ? ORDER BY ano DESC, mes DESC",
        (empresa["id"],),
    )
    rows = cursor.fetchall()
    if not rows:
        print("Nenhuma trava contábil encontrada.")
        pause()
        return
    print(f"{'Mês':<10} {'Ano':<10} {'Situação':<10}")
    print("-" * 30)
    for mes, ano, is_closed in rows:
        situacao = "Fechada" if is_closed else "Aberta"
        print(f"{mes:<10} {ano:<10} {situacao:<10}")
    pause()

def fechar_trava_contabil(conn: sqlite3.Connection, empresa: dict) -> None:
    print("\nFechar Trava Contábil")
    print("-" * 20)
    mes = input("Mês: ").strip()
    ano = input("Ano: ").strip()

    cursor = conn.cursor()
    cursor.execute(
        "UPDATE trava_contabil SET is_closed = 1 WHERE empresa_id = ? AND ano = ? AND mes = ?",
        (empresa["id"], ano, mes),
    )
    if cursor.rowcount == 0:
        pause("Trava Contábil não encontrada.")
    else:
        conn.commit()
        pause("Trava Contábil fechada com sucesso.")

def abrir_trava_contabil(conn: sqlite3.Connection, empresa: dict) -> None:
    print("\nAbrir Trava Contábil")
    print("-" * 20)
    mes = input("Mês: ").strip()
    ano = input("Ano: ").strip()

    cursor = conn.cursor()
    cursor.execute(
        "UPDATE trava_contabil SET is_closed = 0 WHERE empresa_id = ? AND ano = ? AND mes = ?",
        (empresa["id"], ano, mes),
    )
    if cursor.rowcount == 0:
        pause("Trava Contábil não encontrada.")
    else:
        conn.commit()
        pause("Trava Contábil aberta com sucesso.")
