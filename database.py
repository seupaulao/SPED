import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "empresas.db"


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS empresas (
                id    INTEGER PRIMARY KEY AUTOINCREMENT,
                cnpj  TEXT    NOT NULL UNIQUE,
                nome  TEXT    NOT NULL
            )
            """
        )
        conn.commit()


def get_all() -> list[sqlite3.Row]:
    with get_connection() as conn:
        return conn.execute(
            "SELECT id, cnpj, nome FROM empresas ORDER BY nome"
        ).fetchall()


def create(cnpj: str, nome: str) -> None:
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO empresas (cnpj, nome) VALUES (?, ?)", (cnpj, nome)
        )
        conn.commit()


def update(empresa_id: int, cnpj: str, nome: str) -> None:
    with get_connection() as conn:
        conn.execute(
            "UPDATE empresas SET cnpj = ?, nome = ? WHERE id = ?",
            (cnpj, nome, empresa_id),
        )
        conn.commit()


def delete(empresa_id: int) -> None:
    with get_connection() as conn:
        conn.execute("DELETE FROM empresas WHERE id = ?", (empresa_id,))
        conn.commit()
