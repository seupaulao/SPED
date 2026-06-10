from utils import *
from empresa import *
from contas import *
from rich.console import Console
from rich.table import Table
from rich import box

_console = Console()

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
) -> list[dict[str, Any]]:
    print("\nIniciar os lançamentos")
    items: list[dict[str, Any]] = []
    while True:
        raw_account = input("qual a conta? ").strip()
        if raw_account.lower() == "?" or raw_account.lower() == "help":
            print("Digite o nome ou código da conta. Use 'A ' antes do nome para indicar que é um CRÉDITO.")
            listar_contas_empresa(conn, empresa)
            continue
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
                "valor": amount
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
        SELECT id, empresa_id, data, numero, historico
        FROM lancamento
        WHERE empresa_id = ? AND id = ?
        """,
        (empresa_id, lancamento_id),
    )


def fetch_lancamento_items(conn: sqlite3.Connection, lancamento_id: int) -> list[sqlite3.Row]:
    return fetch_all(
        conn,
        """
        SELECT li.id, li.conta_id, li.tipo, li.valor, c.codigo, c.descricao
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
    print("Itens:")
    for item in fetch_lancamento_items(conn, lancamento["id"]):
        print(
            f"  {item['tipo']} | {item['codigo']} - {item['descricao']} | {format_currency(item['valor'])}"
        )


def choose_lancamento(conn: sqlite3.Connection, empresa: sqlite3.Row, action_label: str) -> Optional[sqlite3.Row]:
    visualizar_lancamentos(conn, empresa, pause_after=False)
    code = input(f"\nQual o ID do lançamento que deseja {action_label}? [Digite '.' para voltar ao submenu.] ").strip()
    if code == ".":
        return None
    lancamento = fetch_lancamento(conn, empresa["id"], code)
    if not lancamento:
        pause("Lançamento não encontrado para esta empresa. Clique ENTER para voltar ao submenu.")
        return None
    print_lancamento_detalhes(conn, lancamento)
    return lancamento


def save_lancamento(conn: sqlite3.Connection, empresa_id: int, header: dict[str, Any], items: list[dict[str, Any]]) -> None:
   # total = sum(item["valor"] for item in items if item["tipo"] == "D")
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO lancamento (empresa_id, data, numero, historico)
        VALUES (?, ?, ?, ?)
        """,
        (empresa_id, header["data"], header["numero"], header["historico"]),
    )
    lancamento_id = cur.lastrowid
    for item in items:
        cur.execute(
            """
            INSERT INTO lancamento_item (lancamento_id, conta_id, tipo, valor)
            VALUES (?, ?, ?, ?)
            """,
            (lancamento_id, item["conta_id"], item["tipo"], item["valor"]),
        )


def replace_lancamento(
    conn: sqlite3.Connection,
    empresa_id: int,
    lancamento_id: int,
    header: dict[str, Any],
    items: list[dict[str, Any]],
) -> None:
    conn.execute(
        """
        UPDATE lancamento
        SET data = ?, numero = ?, historico = ?
        WHERE id = ? AND empresa_id = ?
        """,
        (header["data"], header["numero"], header["historico"], lancamento_id, empresa_id),
    )
    conn.execute("DELETE FROM lancamento_item WHERE lancamento_id = ?", (lancamento_id,))
    for item in items:
        conn.execute(
            """
            INSERT INTO lancamento_item (lancamento_id, conta_id, tipo, valor)
            VALUES (?, ?, ?, ?)
            """,
            (lancamento_id, item["conta_id"], item["tipo"], item["valor"]),
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

        items = prompt_lancamento_items(conn, empresa)

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
    items = prompt_lancamento_items(conn, empresa)
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
            _console.print("\nNenhum lançamento encontrado para esta empresa.")
        return

    table = Table(box=box.SIMPLE_HEAVY, show_lines=False)
    table.add_column("ID", justify="right", style="bold", no_wrap=True)
    table.add_column("CODIGO", no_wrap=True)
    table.add_column("DATA", no_wrap=True)
    table.add_column("DESCRICAO")
    table.add_column("TIPO", justify="center", no_wrap=True)
    table.add_column("VALOR", justify="right", no_wrap=True)

    for row in rows:
        tipo = row["tipo"] or ""
        valor = row["valor"]

        tipo_style = "yellow" if tipo == "D" else ("green" if tipo == "C" else "")
        valor_style = "red" if valor < 0 else "blue"

        table.add_row(
            str(row["id"]),
            row["codigo"] or "",
            display_date(row["data"]),
            row["descricao"] or "",
            f"[{tipo_style}]{tipo}[/{tipo_style}]" if tipo_style else tipo,
            f"[{valor_style}]{format_currency(valor)}[/{valor_style}]",
        )

    _console.print(table)
    if pause_after:
        pause()


## TODO - criar lancamentos de estorno e ajuste
def criar_lancamento_estorno(conn, empresa):
    return 

def criar_lancamento_ajuste(conn, empresa):
    return
