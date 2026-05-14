from __future__ import annotations

import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable, Optional

import funcoes_relatorios as relatorios


APP_TITLE = "PJLA Contabilidade OFFLINE"
DB_PATH = Path(__file__).with_name("contabilidade.db")
SCHEMA_PATH = Path(__file__).with_name("banco_sqlite3.sql")
EMPRESA_FIELDS = [
    ("cnpj", "CNPJ", True, "text"),
    ("nome", "NOME", True, "text"),
    ("uf", "UF", False, "text"),
    ("municipio", "MUNICIPIO", False, "text"),
    ("data_inicio", "DATA DE INICIO", False, "date"),
    ("data_fim", "DATA DE FIM", False, "date"),
]


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


def ask_empresa(conn: sqlite3.Connection) -> Optional[sqlite3.Row]:
    total = fetch_one(conn, "SELECT COUNT(*) AS total FROM empresa")
    if not total or total["total"] == 0:
        pause("Não há empresas cadastradas. Cadastre uma Empresa no Menu Principal. Clique ENTER para voltar ao Menu Principal.")
        return None

    termo = input("Qual a empresa? ").strip()
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

        print("\nCODIGO | NOME | CNPJ")
        print("-" * 72)
        for row in rows:
            print(f"{row['id']:>6} | {row['nome']:<30.30} | {row['cnpj']}")

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
        conn.execute("DELETE FROM historico_padrao WHERE empresa_id = ?", (empresa["id"],))
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


def prompt_lancamento_header() -> Optional[dict[str, Any]]:
    print("\nNovo lançamento")
    print("Informe os dados do cabeçalho. Digite '.' para cancelar.")
    raw_date = input("Data do lançamento [DD/MM/AAAA]: ").strip()
    if raw_date == ".":
        return None
    historico = input("Histórico: ").strip()
    if historico == ".":
        return None
    numero = input("Número do documento/operação: ").strip()
    if numero == ".":
        return None
    try:
        data = normalize_date(raw_date)
    except ValueError as exc:
        print(exc)
        return prompt_lancamento_header()
    return {"data": data, "historico": historico or None, "numero": numero or None}


def prompt_lancamento_header_edicao(existing: sqlite3.Row) -> Optional[dict[str, Any]]:
    print("\nCorrigir lançamento")
    print("Tecle ENTER para manter o valor atual ou '.' para cancelar.")

    while True:
        raw_date = input(f"Data do lançamento ({display_date(existing['data'])}): ").strip()
        if raw_date == ".":
            return None
        if raw_date == "":
            data = existing["data"]
            break
        try:
            data = normalize_date(raw_date)
            break
        except ValueError as exc:
            print(exc)

    historico = input(f"Histórico ({existing['historico'] or ''}): ").strip()
    if historico == ".":
        return None

    numero = input(f"Número do documento/operação ({existing['numero'] or ''}): ").strip()
    if numero == ".":
        return None

    return {
        "data": data,
        "historico": existing["historico"] if historico == "" else historico or None,
        "numero": existing["numero"] if numero == "" else numero or None,
    }


def prompt_lancamento_items(
    conn: sqlite3.Connection,
    empresa: sqlite3.Row,
    historico_padrao: Optional[str],
) -> list[dict[str, Any]]:
    print("\nIniciar os lançamentos")
    items: list[dict[str, Any]] = []
    while True:
        raw_account = input("qual a conta? ").strip()
        if raw_account == ".":
            break
        if not raw_account:
            print("Informe uma conta ou '.' para encerrar.")
            continue

        account, entry_type = find_account(conn, empresa["id"], raw_account)
        if not account:
            print("Conta não encontrada para esta empresa.")
            continue
        if account["tipo"] != "A" or not account["aceita_lancamento"]:
            print("Nunca permita lançar em conta sintética. Escolha uma conta analítica.")
            continue

        raw_value = input("valor: ").strip()
        if raw_value == "." or raw_value == "":
            break
        try:
            amount = parse_decimal(raw_value)
        except ValueError as exc:
            print(exc)
            continue

        items.append(
            {
                "conta_id": account["id"],
                "conta_codigo": account["codigo"],
                "conta_descricao": account["descricao"],
                "tipo": entry_type,
                "valor": amount,
                "historico": historico_padrao,
            }
        )
        print(f"{entry_type} | {account['codigo']} - {account['descricao']} | {format_currency(amount)}")
    return items


def summarize_items(items: list[dict[str, Any]]) -> tuple[float, float]:
    total_debitos = sum(item["valor"] for item in items if item["tipo"] == "D")
    total_creditos = sum(item["valor"] for item in items if item["tipo"] == "C")
    return total_debitos, total_creditos


def validate_lancamento_items(items: list[dict[str, Any]]) -> bool:
    if not items:
        return False
    total_debitos, total_creditos = summarize_items(items)
    print(f"\nDébitos: {format_currency(total_debitos)}")
    print(f"Créditos: {format_currency(total_creditos)}")
    return round(total_debitos, 2) == round(total_creditos, 2)


def fetch_lancamento(conn: sqlite3.Connection, empresa_id: int, lancamento_id: Any) -> Optional[sqlite3.Row]:
    return fetch_one(
        conn,
        """
        SELECT id, empresa_id, data, numero, historico, valor_total
        FROM lancamento
        WHERE empresa_id = ? AND id = ?
        """,
        (empresa_id, lancamento_id),
    )


def fetch_lancamento_items(conn: sqlite3.Connection, lancamento_id: int) -> list[sqlite3.Row]:
    return fetch_all(
        conn,
        """
        SELECT li.id, li.conta_id, li.tipo, li.valor, li.historico, c.codigo, c.descricao
        FROM lancamento_item li
        JOIN plano_contas c ON c.id = li.conta_id
        WHERE li.lancamento_id = ?
        ORDER BY li.id
        """,
        (lancamento_id,),
    )


def print_lancamento_detalhes(conn: sqlite3.Connection, lancamento: sqlite3.Row) -> None:
    print("\nLançamento selecionado")
    print(f"ID: {lancamento['id']}")
    print(f"Data: {display_date(lancamento['data'])}")
    print(f"Número: {lancamento['numero'] or ''}")
    print(f"Histórico: {lancamento['historico'] or ''}")
    print(f"Valor total: {format_currency(lancamento['valor_total'])}")
    print("Itens:")
    for item in fetch_lancamento_items(conn, lancamento["id"]):
        print(
            f"  {item['tipo']} | {item['codigo']} - {item['descricao']} | {format_currency(item['valor'])}"
        )


def choose_lancamento(conn: sqlite3.Connection, empresa: sqlite3.Row, action_label: str) -> Optional[sqlite3.Row]:
    visualizar_lancamentos(conn, empresa, pause_after=False)
    code = input(f"\nQual o ID do lançamento que deseja {action_label}? Digite '.' para voltar ao submenu. ").strip()
    if code == ".":
        return None
    lancamento = fetch_lancamento(conn, empresa["id"], code)
    if not lancamento:
        pause("Lançamento não encontrado para esta empresa. Clique ENTER para voltar ao submenu.")
        return None
    print_lancamento_detalhes(conn, lancamento)
    return lancamento


def save_lancamento(conn: sqlite3.Connection, empresa_id: int, header: dict[str, Any], items: list[dict[str, Any]]) -> None:
    total = sum(item["valor"] for item in items if item["tipo"] == "D")
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO lancamento (empresa_id, data, numero, historico, valor_total)
        VALUES (?, ?, ?, ?, ?)
        """,
        (empresa_id, header["data"], header["numero"], header["historico"], total),
    )
    lancamento_id = cur.lastrowid
    for item in items:
        cur.execute(
            """
            INSERT INTO lancamento_item (lancamento_id, conta_id, tipo, valor, historico)
            VALUES (?, ?, ?, ?, ?)
            """,
            (lancamento_id, item["conta_id"], item["tipo"], item["valor"], item["historico"]),
        )


def replace_lancamento(
    conn: sqlite3.Connection,
    empresa_id: int,
    lancamento_id: int,
    header: dict[str, Any],
    items: list[dict[str, Any]],
) -> None:
    total_debitos, _ = summarize_items(items)
    conn.execute(
        """
        UPDATE lancamento
        SET data = ?, numero = ?, historico = ?, valor_total = ?
        WHERE id = ? AND empresa_id = ?
        """,
        (header["data"], header["numero"], header["historico"], total_debitos, lancamento_id, empresa_id),
    )
    conn.execute("DELETE FROM lancamento_item WHERE lancamento_id = ?", (lancamento_id,))
    for item in items:
        conn.execute(
            """
            INSERT INTO lancamento_item (lancamento_id, conta_id, tipo, valor, historico)
            VALUES (?, ?, ?, ?, ?)
            """,
            (lancamento_id, item["conta_id"], item["tipo"], item["valor"], item["historico"]),
        )


def delete_lancamento(conn: sqlite3.Connection, empresa_id: int, lancamento_id: int) -> None:
    conn.execute("DELETE FROM lancamento_item WHERE lancamento_id = ?", (lancamento_id,))
    conn.execute("DELETE FROM lancamento WHERE id = ? AND empresa_id = ?", (lancamento_id, empresa_id))


def criar_lancamento(conn: sqlite3.Connection, empresa: sqlite3.Row) -> None:
    while True:
        print(f"\nEMPRESA: {empresa['id']} - {empresa['nome']}")
        print(empresa["cnpj"])
        header = prompt_lancamento_header()
        if header is None:
            return

        items = prompt_lancamento_items(conn, empresa, header["historico"])

        if not items:
            return

        if not validate_lancamento_items(items):
            pause("Lançamento inválido: a soma dos DÉBITOS deve ser igual à soma dos CRÉDITOS. Clique ENTER para voltar ao submenu.")
            return

        answer = input("Deseja salvar a informação? (s/n) ").strip().lower()
        if answer != "s":
            return

        try:
            conn.execute("BEGIN")
            save_lancamento(conn, empresa["id"], header, items)
            conn.commit()
            print("Lançamento salvo com sucesso.")
        except sqlite3.DatabaseError as exc:
            conn.rollback()
            pause(f"Erro ao salvar lançamento: {exc}. Clique ENTER para voltar ao submenu.")
            return


def corrigir_lancamento(conn: sqlite3.Connection, empresa: sqlite3.Row) -> None:
    lancamento = choose_lancamento(conn, empresa, "CORRIGIR")
    if not lancamento:
        return

    header = prompt_lancamento_header_edicao(lancamento)
    if header is None:
        return

    print("\nOs itens do lançamento serão digitados novamente.")
    items = prompt_lancamento_items(conn, empresa, header["historico"])
    if not items:
        pause("Nenhuma partida informada. Clique ENTER para voltar ao submenu.")
        return
    if not validate_lancamento_items(items):
        pause("Lançamento inválido: a soma dos DÉBITOS deve ser igual à soma dos CRÉDITOS. Clique ENTER para voltar ao submenu.")
        return

    answer = input("Deseja salvar a correção? (s/n) ").strip().lower()
    if answer != "s":
        return

    try:
        conn.execute("BEGIN")
        replace_lancamento(conn, empresa["id"], lancamento["id"], header, items)
        conn.commit()
        pause("Lançamento corrigido com sucesso. Clique ENTER para voltar ao submenu.")
    except sqlite3.DatabaseError as exc:
        conn.rollback()
        pause(f"Erro ao corrigir lançamento: {exc}. Clique ENTER para voltar ao submenu.")


def apagar_lancamento(conn: sqlite3.Connection, empresa: sqlite3.Row) -> None:
    lancamento = choose_lancamento(conn, empresa, "APAGAR")
    if not lancamento:
        return

    answer = input("Deseja apagar esse lançamento? (s/n) ").strip().lower()
    if answer != "s":
        return

    try:
        conn.execute("BEGIN")
        delete_lancamento(conn, empresa["id"], lancamento["id"])
        conn.commit()
        pause("Lançamento apagado com sucesso. Clique ENTER para voltar ao submenu.")
    except sqlite3.DatabaseError as exc:
        conn.rollback()
        pause(f"Erro ao apagar lançamento: {exc}. Clique ENTER para voltar ao submenu.")


def visualizar_lancamentos(conn: sqlite3.Connection, empresa: sqlite3.Row, pause_after: bool = True) -> None:
    rows = fetch_all(
        conn,
        """

        select lan.id, lan.numero, conta.codigo, lan.data, conta.descricao, item.tipo, item.valor 
        from lancamento as lan inner join lancamento_item item on lan.id = item.lancamento_id,
        plano_contas as conta on conta.id = item.conta_id
        where lan.empresa_id = ?
        ORDER BY lan.data DESC, lan.id DESC
        LIMIT 10
        """,
        (empresa["id"],),
    )
    if not rows:
        if pause_after:
            pause("Nenhum lançamento encontrado para esta empresa. Clique ENTER para voltar ao submenu.")
        else:
            print("\nNenhum lançamento encontrado para esta empresa.")
        return

    print("\nID | NUMERO | CODIGO | DATA | DESCRICAO | TIPO | VALOR")
    print("-" * 90)
    for row in rows:
        print(
            f"{row['id']:>2} | {(row['numero'] or ''):<10.10} | {(row['codigo'] or ''):<10.10} | {display_date(row['data'])} | "
            f"{(row['descricao'] or ''):<40.40} | {(row['tipo'] or ''):<5.5} | {format_currency(row['valor'])}"
        )
    if pause_after:
        pause()


def menu_livro_diario(conn: sqlite3.Connection) -> None:
    empresa = ask_empresa(conn)
    if not empresa:
        return
    while True:
        print("\n[a] Criar Lançamento")
        print("[b] Corrigir Lançamento")
        print("[c] Apagar Lançamento")
        print("[d] Visualizar todos os Lançamentos")
        print("[e] Voltar ao menu principal")
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
            return
        else:
            pause("Opção inválida. Clique ENTER para tentar novamente.")


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


def menu_relatorios(conn: sqlite3.Connection) -> None:
    empresa = ask_empresa(conn)
    if not empresa:
        return
    while True:
        print("\n[b] Balancete")
        print("[c] Balanço Patrimonial")
        print("[d] DRE")
        print("[e] DVA")
        print("[f] Voltar")
        choice = input("\nEscolha: ").strip().lower()
        if choice == "f":
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
            elif choice == "q":
                return
            else:
                pause("Opção inválida. Clique ENTER para tentar novamente.")
    finally:
        conn.close()


if __name__ == "__main__":
    main()