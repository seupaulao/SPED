from datetime import datetime
from typing import Any, Iterable, Optional
import sqlite3
from pathlib import Path

APP_TITLE = "PJLA Contabilidade OFFLINE"
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "contabilidade_simples.db"
SCHEMA_PATH = BASE_DIR / "banco_sqlite3.sql"

def pause(message: str = "Clique ENTER para continuar.") -> None:
    input(f"\n{message}")


def normalize_date(value: str) -> str:
    text = value.strip()
    if not text:
        return ""
    for fmt in ("%d/%m/%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(text, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    raise ValueError("Use o formato DD/MM/AAAA.")


def display_date(value: Optional[str]) -> str:
    if not value:
        return ""
    for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
        try:
            return datetime.strptime(value, fmt).strftime("%d/%m/%Y")
        except ValueError:
            continue
    return value


def parse_decimal(value: str) -> float:
    text = value.strip()
    if "," in text and "." in text:
        if text.rfind(",") > text.rfind("."):
            text = text.replace(".", "").replace(",", ".")
        else:
            text = text.replace(",", "")
    elif "," in text:
        text = text.replace(".", "").replace(",", ".")
    if not text:
        raise ValueError("Informe um valor numérico.")
    amount = float(text)
    if amount <= 0:
        raise ValueError("Informe um valor maior que zero.")
    return amount


def format_currency(value: Any) -> str:
    amount = float(value or 0.0)
    text = f"{amount:,.2f}"
    return text.replace(",", "X").replace(".", ",").replace("X", ".")


def print_header() -> None:
    print(f"\n{APP_TITLE}")
    print("=" * len(APP_TITLE))


def connect_db() -> sqlite3.Connection:
    db_exists = DB_PATH.exists()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    ensure_runtime_schema(conn, db_exists=db_exists)
    return conn


def ensure_runtime_schema(conn: sqlite3.Connection, db_exists: bool) -> None:
    if not db_exists and SCHEMA_PATH.exists():
        conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
        conn.commit()

    columns = {row[1] for row in conn.execute("PRAGMA table_info(plano_contas)").fetchall()}
    extra_columns = {
        "grupo": "TEXT",
        "dre_grupo": "TEXT",
        "subgrupo": "TEXT",
        "fluxo_caixa_tipo": "TEXT",
    }
    for column_name, column_type in extra_columns.items():
        if column_name not in columns:
            conn.execute(f"ALTER TABLE plano_contas ADD COLUMN {column_name} {column_type}")

    conn.execute("CREATE INDEX IF NOT EXISTS idx_lancamento_data ON lancamento(data)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_lancamento_item_conta ON lancamento_item(conta_id)")
    conn.commit()


def fetch_one(conn: sqlite3.Connection, sql: str, params: Iterable[Any] = ()) -> Optional[sqlite3.Row]:
    return conn.execute(sql, tuple(params)).fetchone()


def fetch_all(conn: sqlite3.Connection, sql: str, params: Iterable[Any] = ()) -> list[sqlite3.Row]:
    return conn.execute(sql, tuple(params)).fetchall()

def find_account(conn: sqlite3.Connection, empresa_id: int, raw_name: str) -> tuple[Optional[sqlite3.Row], str]:
    normalized = raw_name.strip()
    entry_type = "D"
    if normalized.lower().startswith("a "):
        entry_type = "C"
        normalized = normalized[2:].strip()

    account = fetch_one(
        conn,
        """
        SELECT *
        FROM plano_contas
        WHERE empresa_id = ?
          AND (UPPER(descricao) = UPPER(?) OR codigo = ? OR UPPER(descricao) LIKE UPPER(?))
        ORDER BY CASE
            WHEN UPPER(descricao) = UPPER(?) THEN 0
            WHEN codigo = ? THEN 1
            ELSE 2
        END,
        codigo
        LIMIT 1
        """,
        (empresa_id, normalized, normalized, f"%{normalized}%", normalized, normalized),
    )
    return account, entry_type


def ask_period() -> Optional[tuple[str, str]]:
    print("\nIndique o Período:")
    raw_start = input("De: [Formato DD/MM/AAAA] ").strip()
    raw_end = input("Até: [Formato DD/MM/AAAA] ").strip()
    if not raw_start or not raw_end:
        pause("Informe a data inicial e a data final no formato DD/MM/AAAA.")
        return None
    try:
        return normalize_date(raw_start), normalize_date(raw_end)
    except ValueError as exc:
        pause(str(exc))
        return None


def print_rows(title: str, rows: list[dict[str, Any]]) -> None:
    print(f"\n{title}")
    print("-" * len(title))
    if not rows:
        print("Sem dados para o período informado.")
        return
    for row in rows:
        print(
            f"{row.get('codigo', ''):<12} | {row.get('descricao', ''):<40.40} | "
            f"D {format_currency(row.get('debitos')):<12} | "
            f"C {format_currency(row.get('creditos')):<12} | "
            f"S {format_currency(row.get('saldo'))}"
        )


def print_key_values(title: str, values: dict[str, Any]) -> None:
    print(f"\n{title}")
    print("-" * len(title))
    for key, value in values.items():
        if isinstance(value, dict):
            print(f"{key}:")
            for sub_key, sub_value in value.items():
                print(f"  {sub_key}: {format_currency(sub_value)}")
        elif isinstance(value, list):
            print(f"{key}: {len(value)} contas")
        else:
            print(f"{key}: {format_currency(value)}")

def ask_empresa(conn: sqlite3.Connection) -> Optional[sqlite3.Row]:
    total = fetch_one(conn, "SELECT COUNT(*) AS total FROM empresa")
    if not total or total["total"] == 0:
        pause("Não há empresas cadastradas. Cadastre uma Empresa no Menu Principal. Clique ENTER para voltar ao Menu Principal.")
        return None

    termo = input("Qual a empresa? [Digite '?' para listar todas] ").strip()
    if termo == "?":
        empresas = fetch_all(conn, "SELECT id, nome FROM empresa ORDER BY nome")
        print("\nEmpresas Cadastradas:")
        for e in empresas:
            print(f"{e['id']}: {e['nome']}")
        termo = input("\nDigite o ID ou o nome da Empresa: ").strip()
    if not termo:
        pause("Não encontrei nenhuma empresa cadastrada com os dados digitados. Clique ENTER para voltar ao Menu Principal.")
        return None

    empresa = fetch_one(
        conn,
        """
        SELECT *
        FROM empresa
        WHERE CAST(id AS TEXT) = ?
           OR cnpj = ?
           OR UPPER(nome) = UPPER(?)
           OR UPPER(nome) LIKE UPPER(?)
        ORDER BY CASE
            WHEN CAST(id AS TEXT) = ? THEN 0
            WHEN cnpj = ? THEN 1
            WHEN UPPER(nome) = UPPER(?) THEN 2
            ELSE 3
        END,
        id
        LIMIT 1
        """,
        (termo, termo, termo, f"%{termo}%", termo, termo, termo),
    )
    if not empresa:
        pause("Não encontrei nenhuma empresa cadastrada com os dados digitados. Clique ENTER para voltar ao Menu Principal.")
        return None

    print(f"\nEMPRESA: {empresa['id']} - {empresa['nome']}")
    print(empresa["cnpj"])
    return empresa

def ask_tomador(conn: sqlite3.Connection) -> Optional[sqlite3.Row]:
    termo = input("Qual o Tomador? [Digite '?' para listar todos] ").strip()
    if termo == "?":
        tomadores = fetch_all(conn, "SELECT id, nome FROM tomador ORDER BY nome")
        if not tomadores:
            pause("Não há tomadores cadastrados. Cadastre um Tomador no Menu Principal. Clique ENTER para voltar ao Menu Principal.")
            return None
        print("\nTomadores Cadastrados:")
        for t in tomadores:
            print(f"{t['id']}: {t['nome']}")
        termo = input("\nDigite o ID ou o nome do Tomador: ").strip()
    if not termo:
        pause("Não encontrei nenhum tomador cadastrado com os dados digitados. Clique ENTER para voltar ao Menu Principal.")
        return None

    tomador = fetch_one(
        conn,
        """
        SELECT *
        FROM tomador
        WHERE CAST(id AS TEXT) = ?
           OR cnpj = ?
           OR UPPER(nome) = UPPER(?)
           OR UPPER(nome) LIKE UPPER(?)
        ORDER BY CASE
            WHEN CAST(id AS TEXT) = ? THEN 0
            WHEN cnpj = ? THEN 1
            WHEN UPPER(nome) = UPPER(?) THEN 2
            ELSE 3
        END,
        id
        LIMIT 1
        """,
        (termo, termo, termo, f"%{termo}%", termo, termo, termo),
    )
    if not tomador:
        pause("Não encontrei nenhum tomador cadastrado com os dados digitados. Clique ENTER para voltar ao Menu Principal.")
        return None

    print(f"\nTOMADOR: {tomador['id']} - {tomador['nome']}")
    print(tomador["cnpj"])
    return tomador