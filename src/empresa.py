from datetime import datetime
from typing import Any, Iterable, Optional
import sqlite3
from pathlib import Path
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

def is_empresa_table_empty(conn: sqlite3.Connection) -> bool:
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM empresa")
    count = cursor.fetchone()[0]
    return count == 0

def collect_empresa_data(existing: Optional[sqlite3.Row] = None) -> Optional[dict[str, Any]]:
    values: dict[str, Any] = {}
    for field_name, label, required, field_type in EMPRESA_FIELDS:
        while True:
            if existing is None:
                prompt = f"{label}: "
            else:
                current_value = display_date(existing[field_name]) if field_type == "date" else (existing[field_name] or "")
                print(f"Digite o novo {label} da empresa, ou tecle ENTER para CONFIRMAR o valor atual")
                prompt = f"{label} ({current_value}): "

            raw_value = input(prompt).strip()
            if existing is not None and raw_value == "":
                values[field_name] = existing[field_name]
                break

            if raw_value == "" and not required:
                values[field_name] = None
                break

            if raw_value == "" and required:
                print(f"O campo {label} é obrigatório.")
                continue

            try:
                if field_type == "date":
                    values[field_name] = normalize_date(raw_value)
                else:
                    values[field_name] = raw_value
                break
            except ValueError as exc:
                print(exc)
    answer = input("Deseja salvar a informação? (s/n) ").strip().lower()
    if answer != "s":
        return None
    return values


def cadastrar_empresa(conn: sqlite3.Connection) -> None:
    values = collect_empresa_data()
    if values is None:
        return
    try:
        conn.execute(
            """
            INSERT INTO empresa (cnpj, nome, uf, municipio, data_inicio, data_fim)
            VALUES (:cnpj, :nome, :uf, :municipio, :data_inicio, :data_fim)
            """,
            values,
        )
        conn.commit()
        pause("Empresa salva com sucesso. Clique ENTER para voltar ao submenu.")
    except sqlite3.DatabaseError as exc:
        conn.rollback()
        pause(f"Erro ao salvar: {exc}. Clique ENTER para voltar ao submenu.")


def listar_empresas(conn: sqlite3.Connection) -> None:
    page = 0
    page_size = 10
    while True:
        rows = fetch_all(
            conn,
            "SELECT id, nome, cnpj FROM empresa ORDER BY id LIMIT ? OFFSET ?",
            (page_size, page * page_size),
        )
        if not rows and page == 0:
            pause("Nenhuma empresa cadastrada. Clique ENTER para voltar ao submenu.")
            return
        if not rows:
            page -= 1
            continue

        table = Table(box=box.SIMPLE_HEAVY, show_lines=False)
        table.add_column("CODIGO", justify="right", no_wrap=True)
        table.add_column("NOME")
        table.add_column("CNPJ", no_wrap=True)

        for row in rows:
            table.add_row(str(row["id"]), row["nome"] or "", row["cnpj"] or "")

        _console.print(table)

        command = input("\n[N] próxima página | [P] página anterior | [ENTER] voltar: ").strip().lower()
        if command == "n":
            page += 1
            continue
        if command == "p" and page > 0:
            page -= 1
            continue
        return


def alterar_empresa(conn: sqlite3.Connection) -> None:
    code = input("Qual o CODIGO da EMPRESA que deseja ALTERAR? Digite '.' para voltar ao submenu. ").strip()
    if code == ".":
        return
    empresa = fetch_one(conn, "SELECT * FROM empresa WHERE id = ?", (code,))
    if not empresa:
        pause("Empresa não encontrada. Clique ENTER para voltar ao submenu.")
        return
    values = collect_empresa_data(existing=empresa)
    if values is None:
        return
    values["id"] = empresa["id"]
    try:
        conn.execute(
            """
            UPDATE empresa
            SET cnpj = :cnpj,
                nome = :nome,
                uf = :uf,
                municipio = :municipio,
                data_inicio = :data_inicio,
                data_fim = :data_fim
            WHERE id = :id
            """,
            values,
        )
        conn.commit()
        pause("Empresa alterada com sucesso. Clique ENTER para voltar ao submenu.")
    except sqlite3.DatabaseError as exc:
        conn.rollback()
        pause(f"Erro ao alterar: {exc}. Clique ENTER para voltar ao submenu.")


def excluir_empresa(conn: sqlite3.Connection) -> None:
    code = input("Qual o CODIGO da EMPRESA que deseja EXCLUIR? Digite '.' para voltar ao submenu. ").strip()
    if code == ".":
        return
    empresa = fetch_one(conn, "SELECT * FROM empresa WHERE id = ?", (code,))
    if not empresa:
        pause("Empresa não encontrada. Clique ENTER para voltar ao submenu.")
        return

    print(f"\nEMPRESA: {empresa['id']} - {empresa['nome']}")
    print(empresa["cnpj"])
    answer = input("Deseja excluir essa entidade e TODOS seus dados? (s/n) ").strip().lower()
    if answer != "s":
        return

    try:
        conn.execute("BEGIN")
        conn.execute(
            "DELETE FROM mapa_demonstracoes WHERE conta_id IN (SELECT id FROM plano_contas WHERE empresa_id = ?)",
            (empresa["id"],),
        )
        conn.execute(
            "DELETE FROM lancamento_item WHERE lancamento_id IN (SELECT id FROM lancamento WHERE empresa_id = ?)",
            (empresa["id"],),
        )
        conn.execute("DELETE FROM lancamento WHERE empresa_id = ?", (empresa["id"],))

        conn.execute("DELETE FROM plano_contas WHERE empresa_id = ?", (empresa["id"],))
        conn.execute("DELETE FROM empresa WHERE id = ?", (empresa["id"],))
        conn.commit()
        pause("Empresa excluída com sucesso. Clique ENTER para voltar ao submenu.")
    except sqlite3.DatabaseError as exc:
        conn.rollback()
        pause(f"Erro ao excluir: {exc}. Clique ENTER para voltar ao submenu.")


def menu_cadastro_empresa(conn: sqlite3.Connection) -> None:
    while True:
        print_header()
        print("[a] Cadastrar")
        print("[b] Alterar")
        print("[c] Listar")
        print("[d] Excluir")
        print("[f] Voltar")
        choice = input("\nEscolha: ").strip().lower()
        if choice == "a":
            cadastrar_empresa(conn)
        elif choice == "b":
            alterar_empresa(conn)
        elif choice == "c":
            listar_empresas(conn)
        elif choice == "d":
            excluir_empresa(conn)
        elif choice == "f":
            return
        else:
            pause("Opção inválida. Clique ENTER para tentar novamente.")

