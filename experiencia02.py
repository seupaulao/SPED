from __future__ import annotations

import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable, Optional

from textual.app import ComposeResult, SystemCommand
from textual.containers import Container, Horizontal, Vertical, ScrollableContainer
from textual.widgets import Header, Footer, Button, Label, Input, Static, DataTable, Select, TextArea
from textual.screen import Screen
from textual.app import App
from textual.binding import Binding

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


# ============= DATABASE FUNCTIONS =============

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
        SELECT li.id, li.conta_id, li.tipo, li.valor, li.historico, c.codigo, c.descricao
        FROM lancamento_item li
        JOIN plano_contas c ON c.id = li.conta_id
        WHERE li.lancamento_id = ?
        ORDER BY li.id
        """,
        (lancamento_id,),
    )


def summarize_items(items: list[dict[str, Any]]) -> tuple[float, float]:
    total_debitos = sum(item["valor"] for item in items if item["tipo"] == "D")
    total_creditos = sum(item["valor"] for item in items if item["tipo"] == "C")
    return total_debitos, total_creditos


# ============= TEXTUAL UI COMPONENTS =============

class FormField(Container):
    """Form field component with label and input."""
    
    def __init__(self, label: str, field_type: str = "text", required: bool = False, value: str = "", **kwargs):
        super().__init__(**kwargs)
        self.label = label
        self.field_type = field_type
        self.required = required
        self.value = value
        self.input_widget: Optional[Input] = None

    def compose(self) -> ComposeResult:
        yield Label(f"{self.label}{'*' if self.required else ''}")
        if self.field_type == "text":
            self.input_widget = Input(value=self.value, id=self.label.lower().replace(" ", "_"))
            yield self.input_widget
        elif self.field_type == "date":
            self.input_widget = Input(value=self.value, placeholder="DD/MM/AAAA", id=self.label.lower().replace(" ", "_"))
            yield self.input_widget

    def get_value(self) -> str:
        return self.input_widget.value if self.input_widget else ""


class EmpresaForm(Static):
    """Form for empresa data entry."""
    
    def __init__(self, existing: Optional[sqlite3.Row] = None, **kwargs):
        super().__init__(**kwargs)
        self.existing = existing
        self.form_fields: dict[str, FormField] = {}

    def compose(self) -> ComposeResult:
        yield Label("Informações da Empresa")
        with ScrollableContainer():
            for field_name, label, required, field_type in EMPRESA_FIELDS:
                value = ""
                if self.existing:
                    val = self.existing[field_name]
                    if field_type == "date" and val:
                        value = display_date(val)
                    elif val:
                        value = str(val)
                
                form_field = FormField(label, field_type=field_type, required=required, value=value)
                self.form_fields[field_name] = form_field
                yield form_field

    def get_data(self) -> dict[str, Any]:
        data = {}
        for field_name, label, required, field_type in EMPRESA_FIELDS:
            form_field = self.form_fields[field_name]
            value = form_field.get_value().strip()
            
            if not value and required:
                raise ValueError(f"Campo '{label}' é obrigatório.")
            
            if field_type == "date" and value:
                value = normalize_date(value)
            
            data[field_name] = value or None
        
        return data


class ContaForm(Static):
    """Form for conta data entry."""
    
    def __init__(self, existing: Optional[sqlite3.Row] = None, **kwargs):
        super().__init__(**kwargs)
        self.existing = existing
        self.fields: dict[str, Input] = {}

    def compose(self) -> ComposeResult:
        yield Label("Dados da Conta")
        with ScrollableContainer():
            field_configs = [
                ("empresa_id", "Código da Empresa", True),
                ("codigo", "Código da Conta (01.01.01)", True),
                ("descricao", "Descrição", True),
                ("tipo", "Tipo [A/S]", True),
                ("natureza", "Natureza [D/C]", True),
                ("grupo", "Grupo", False),
                ("dre_grupo", "Grupo DRE", False),
                ("subgrupo", "Subgrupo", False),
                ("fluxo_caixa_tipo", "Tipo Fluxo Caixa", False),
                ("nivel", "Nível", False),
                ("conta_pai_id", "Conta PAI", False),
                ("codigo_referencial", "Código Referencial", False),
            ]
            
            for field_id, label, required in field_configs:
                value = ""
                if self.existing and field_id in self.existing.keys():
                    val = self.existing[field_id]
                    value = str(val) if val else ""
                
                with Horizontal():
                    yield Label(f"{label}{'*' if required else ''}", classes="label")
                    input_field = Input(value=value, id=field_id)
                    self.fields[field_id] = input_field
                    yield input_field

    def get_data(self) -> dict[str, Any]:
        data = {}
        required_fields = ["empresa_id", "codigo", "descricao", "tipo", "natureza"]
        
        for field_id, input_widget in self.fields.items():
            value = input_widget.value.strip()
            if not value and field_id in required_fields:
                raise ValueError(f"Campo {field_id} é obrigatório.")
            data[field_id] = value or None
        
        return data


class MessageBox(Screen):
    """Simple message display screen."""
    
    def __init__(self, title: str, message: str, **kwargs):
        super().__init__(**kwargs)
        self.title_text = title
        self.message_text = message

    def compose(self) -> ComposeResult:
        with Container():
            yield Label(self.title_text)
            yield Label(self.message_text)
            with Horizontal():
                yield Button("OK", id="btn_ok")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn_ok":
            self.app.pop_screen()


class EmpresaListScreen(Screen):
    """Screen for listing empresas."""
    
    BINDINGS = [
        Binding("escape", "app.pop_screen", "Voltar"),
    ]

    def __init__(self, conn: sqlite3.Connection, **kwargs):
        super().__init__(**kwargs)
        self.conn = conn

    def compose(self) -> ComposeResult:
        yield Header()
        yield DataTable(id="empresa_table")
        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns("ID", "Nome", "CNPJ")
        
        rows = fetch_all(self.conn, "SELECT id, nome, cnpj FROM empresa ORDER BY id")
        for row in rows:
            table.add_row(str(row["id"]), row["nome"], row["cnpj"])


class EmpresaFormScreen(Screen):
    """Screen for empresa form."""
    
    BINDINGS = [
        Binding("escape", "app.pop_screen", "Cancelar"),
        Binding("ctrl+s", "save", "Salvar"),
    ]

    def __init__(self, conn: sqlite3.Connection, existing: Optional[sqlite3.Row] = None, **kwargs):
        super().__init__(**kwargs)
        self.conn = conn
        self.existing = existing

    def compose(self) -> ComposeResult:
        yield Header()
        with Container():
            yield EmpresaForm(existing=self.existing, id="empresa_form")
            with Horizontal():
                yield Button("Salvar", id="btn_save", variant="primary")
                yield Button("Cancelar", id="btn_cancel")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn_save":
            self.action_save()
        elif event.button.id == "btn_cancel":
            self.app.pop_screen()

    def action_save(self) -> None:
        try:
            form = self.query_one(EmpresaForm)
            data = form.get_data()
            
            if self.existing:
                data["id"] = self.existing["id"]
                self.conn.execute(
                    """
                    UPDATE empresa
                    SET cnpj = :cnpj, nome = :nome, uf = :uf, municipio = :municipio,
                        data_inicio = :data_inicio, data_fim = :data_fim
                    WHERE id = :id
                    """,
                    data,
                )
            else:
                self.conn.execute(
                    """
                    INSERT INTO empresa (cnpj, nome, uf, municipio, data_inicio, data_fim)
                    VALUES (:cnpj, :nome, :uf, :municipio, :data_inicio, :data_fim)
                    """,
                    data,
                )
            
            self.conn.commit()
            self.app.notify("Empresa salva com sucesso!")
            self.app.pop_screen()
        except ValueError as e:
            self.app.notify(f"Erro: {str(e)}", severity="error")
        except sqlite3.DatabaseError as e:
            self.conn.rollback()
            self.app.notify(f"Erro ao salvar: {str(e)}", severity="error")


class ContaFormScreen(Screen):
    """Screen for conta form."""
    
    BINDINGS = [
        Binding("escape", "app.pop_screen", "Cancelar"),
        Binding("ctrl+s", "save", "Salvar"),
    ]

    def __init__(self, conn: sqlite3.Connection, existing: Optional[sqlite3.Row] = None, **kwargs):
        super().__init__(**kwargs)
        self.conn = conn
        self.existing = existing

    def compose(self) -> ComposeResult:
        yield Header()
        with Container():
            yield ContaForm(existing=self.existing, id="conta_form")
            with Horizontal():
                yield Button("Salvar", id="btn_save", variant="primary")
                yield Button("Cancelar", id="btn_cancel")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn_save":
            self.action_save()
        elif event.button.id == "btn_cancel":
            self.app.pop_screen()

    def action_save(self) -> None:
        try:
            form = self.query_one(ContaForm)
            data = form.get_data()
            data["aceita_lancamento"] = 1
            
            if self.existing:
                data["id"] = self.existing["id"]
                self.conn.execute(
                    """
                    UPDATE plano_contas
                    SET empresa_id = ?, codigo = ?, descricao = ?, tipo = ?, natureza = ?,
                        grupo = ?, dre_grupo = ?, subgrupo = ?, fluxo_caixa_tipo = ?,
                        nivel = ?, conta_pai_id = ?, codigo_referencial = ?
                    WHERE id = ?
                    """,
                    (data.get("empresa_id"), data.get("codigo"), data.get("descricao"),
                     data.get("tipo"), data.get("natureza"), data.get("grupo"),
                     data.get("dre_grupo"), data.get("subgrupo"), data.get("fluxo_caixa_tipo"),
                     data.get("nivel"), data.get("conta_pai_id"), data.get("codigo_referencial"),
                     data.get("id")),
                )
            else:
                self.conn.execute(
                    """
                    INSERT INTO plano_contas
                    (empresa_id, codigo, descricao, tipo, natureza, grupo, dre_grupo,
                     subgrupo, fluxo_caixa_tipo, nivel, conta_pai_id, codigo_referencial, aceita_lancamento)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (data.get("empresa_id"), data.get("codigo"), data.get("descricao"),
                     data.get("tipo"), data.get("natureza"), data.get("grupo"),
                     data.get("dre_grupo"), data.get("subgrupo"), data.get("fluxo_caixa_tipo"),
                     data.get("nivel"), data.get("conta_pai_id"), data.get("codigo_referencial"),
                     data.get("aceita_lancamento")),
                )
            
            self.conn.commit()
            self.app.notify("Conta salva com sucesso!")
            self.app.pop_screen()
        except ValueError as e:
            self.app.notify(f"Erro: {str(e)}", severity="error")
        except sqlite3.DatabaseError as e:
            self.conn.rollback()
            self.app.notify(f"Erro ao salvar: {str(e)}", severity="error")


class ContaListScreen(Screen):
    """Screen for listing contas."""
    
    BINDINGS = [
        Binding("escape", "app.pop_screen", "Voltar"),
        Binding("n", "nova_conta", "Nova"),
        Binding("e", "editar", "Editar"),
    ]

    def __init__(self, conn: sqlite3.Connection, **kwargs):
        super().__init__(**kwargs)
        self.conn = conn

    def compose(self) -> ComposeResult:
        yield Header()
        yield DataTable(id="conta_table")
        yield Footer()

    def on_mount(self) -> None:
        self.load_contas()

    def load_contas(self) -> None:
        table = self.query_one(DataTable)
        table.clear()
        table.add_columns("Código", "Descrição", "Tipo", "Natureza")
        
        rows = fetch_all(self.conn, "SELECT codigo, descricao, tipo, natureza FROM plano_contas ORDER BY codigo")
        for row in rows:
            table.add_row(row["codigo"], row["descricao"], row["tipo"], row["natureza"])

    def action_nova_conta(self) -> None:
        self.app.push_screen(ContaFormScreen(self.conn))

    def action_editar(self) -> None:
        table = self.query_one(DataTable)
        if table.cursor_row is not None:
            codigo = table.get_cell(table.cursor_row, 0)
            conta = fetch_one(self.conn, "SELECT * FROM plano_contas WHERE codigo = ?", (codigo,))
            if conta:
                self.app.push_screen(ContaFormScreen(self.conn, existing=conta))


class MainScreen(Screen):
    """Main menu screen."""
    
    BINDINGS = [
        Binding("q", "quit", "Sair"),
        Binding("a", "livro_diario", "Livro Diário"),
        Binding("b", "relatorios", "Relatórios"),
        Binding("c", "cadastro_empresa", "Empresa"),
        Binding("e", "plano_contas", "Contas"),
    ]

    def __init__(self, conn: sqlite3.Connection, **kwargs):
        super().__init__(**kwargs)
        self.conn = conn

    def compose(self) -> ComposeResult:
        yield Header()
        with Container():
            yield Label("PJLA Contabilidade OFFLINE", id="title")
            with Vertical(classes="menu"):
                yield Button("[A] Livro Diário", id="btn_livro_diario", variant="primary")
                yield Button("[B] Relatórios", id="btn_relatorios")
                yield Button("[C] Cadastro de Empresa", id="btn_empresa")
                yield Button("[E] Plano de Contas", id="btn_plano_contas")
                yield Button("[Q] Sair", id="btn_quit", variant="error")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn_livro_diario":
            self.action_livro_diario()
        elif event.button.id == "btn_relatorios":
            self.action_relatorios()
        elif event.button.id == "btn_empresa":
            self.action_cadastro_empresa()
        elif event.button.id == "btn_plano_contas":
            self.action_plano_contas()
        elif event.button.id == "btn_quit":
            self.app.action_quit()

    def action_livro_diario(self) -> None:
        self.app.notify("Livro Diário em desenvolvimento")

    def action_relatorios(self) -> None:
        self.app.notify("Relatórios em desenvolvimento")

    def action_cadastro_empresa(self) -> None:
        self.app.push_screen(EmpresaListScreen(self.conn))

    def action_plano_contas(self) -> None:
        self.app.push_screen(ContaListScreen(self.conn))


# ============= MAIN APP =============

class ContabilidadeApp(App):
    """Main application."""
    
    TITLE = "PJLA Contabilidade OFFLINE"
    CSS = """
    Screen {
        layout: vertical;
    }
    
    #title {
        width: 100%;
        height: 3;
        content-align: center middle;
        background: $accent;
        color: $text;
    }
    
    .menu {
        align: center middle;
        width: 40;
        height: auto;
    }
    
    .menu Button {
        width: 100%;
        margin: 1 0;
    }
    
    Label {
        width: 100%;
    }
    
    FormField {
        height: auto;
        margin: 1 0;
    }
    
    FormField Label {
        width: 20;
        margin-right: 1;
    }
    
    Input {
        width: 60;
    }
    
    DataTable {
        height: 1fr;
    }
    
    .label {
        width: 25;
        text-align: right;
        margin-right: 1;
    }
    """

    def __init__(self):
        super().__init__()
        self.conn = connect_db()

    def on_mount(self) -> None:
        self.push_screen(MainScreen(self.conn))

    def on_unmount(self) -> None:
        self.conn.close()


if __name__ == "__main__":
    app = ContabilidadeApp()
    app.run()
