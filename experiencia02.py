from __future__ import annotations

import sqlite3
from datetime import datetime

from typing import Any, Callable, Optional

from textual.app import ComposeResult, SystemCommand
from textual.containers import Container, Horizontal, Vertical, ScrollableContainer
from textual.widgets import Header, Footer, Button, Label, Input, Static, DataTable, Select, TextArea
from textual.screen import Screen
from textual.app import App
from textual.binding import Binding

import funcoes_relatorios as relatorios


APP_TITLE = "PJLA Contabilidade OFFLINE"
EMPRESA_ATUAL: Optional[sqlite3.Row] = None


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


class ConfirmDialog(Screen):
    """Confirmation dialog screen."""

    BINDINGS = [
        Binding("escape", "app.pop_screen", "Cancelar"),
    ]

    def __init__(self, title: str, message: str, on_confirm: Callable[[], None], **kwargs):
        super().__init__(**kwargs)
        self.title_text = title
        self.message_text = message
        self.on_confirm = on_confirm

    def compose(self) -> ComposeResult:
        with Container():
            yield Label(self.title_text)
            yield Label(self.message_text)
            with Horizontal():
                yield Button("Sim", id="btn_yes", variant="primary")
                yield Button("Não", id="btn_no", variant="error")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn_yes":
            self.on_confirm()
            self.app.pop_screen()
        elif event.button.id == "btn_no":
            self.app.pop_screen()


# ============= FORMS =============

class EmpresaForm(Static):
    """Form for empresa data entry."""
    
    def __init__(self, existing: Optional[sqlite3.Row] = None, **kwargs):
        super().__init__(**kwargs)
        self.existing = existing
        self.form_fields: dict[str, FormField] = {}

    def compose(self) -> ComposeResult:
        yield Label("Informações da Empresa")
        with ScrollableContainer():
            for field_name, label, required, field_type in relatorios.EMPRESA_FIELDS:
                value = ""
                if self.existing:
                    val = self.existing[field_name]
                    if field_type == "date" and val:
                        value = relatorios.display_date(val)
                    elif val:
                        value = str(val)
                
                form_field = FormField(label, field_type=field_type, required=required, value=value)
                self.form_fields[field_name] = form_field
                yield form_field

    def get_data(self) -> dict[str, Any]:
        data = {}
        for field_name, label, required, field_type in relatorios.EMPRESA_FIELDS:
            form_field = self.form_fields[field_name]
            value = form_field.get_value().strip()
            
            if not value and required:
                raise ValueError(f"Campo '{label}' é obrigatório.")
            
            if field_type == "date" and value:
                value = relatorios.normalize_date(value)
            
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


# ============= SCREENS =============

class EmpresaListScreen(Screen):
    """Screen for listing empresas."""
    
    BINDINGS = [
        Binding("escape", "app.pop_screen", "Voltar"),
        Binding("n", "nova_empresa", "Novo"),
        Binding("e", "editar_empresa", "Editar"),
        Binding("d", "excluir_empresa", "Excluir"),
    ]

    def __init__(self, conn: sqlite3.Connection, **kwargs):
        super().__init__(**kwargs)
        self.conn = conn

    def compose(self) -> ComposeResult:
        yield Header()
        yield DataTable(id="empresa_table")
        with Horizontal():
            yield Button("Novo", id="btn_novo", variant="primary")
            ##yield Button("Editar", id="btn_editar")
            yield Button("Excluir", id="btn_excluir", variant="error")
        yield Footer()

    def on_mount(self) -> None:
        self.load_empresas()

    def load_empresas(self) -> None:
        table = self.query_one(DataTable)
        table.clear()
        table.add_columns("ID", "Nome", "CNPJ")
        table.cursor_type = "row"

        rows = relatorios.fetch_all(self.conn, "SELECT id, nome, cnpj FROM empresa ORDER BY id")
        for row in rows:
            table.add_row(str(row["id"]), row["nome"], row["cnpj"])

    def get_selected_empresa_id(self) -> Optional[int]:
        table = self.query_one(DataTable)
        table.cursor_type = "row"
        if table.cursor_row is None:
            return None
        print(f"Cursor Row: {table.cursor_row}")    
        selected_id = table.get_cell(table.cursor_row, 0)
        try:
            return int(selected_id)
        except (TypeError, ValueError):
            print("Deu erro ao tentar pegar o ID da empresa selecionada:", selected_id)
            return None

    def action_nova_empresa(self) -> None:
        self.app.push_screen(EmpresaFormScreen(self.conn))

    def action_editar_empresa(self) -> None:
        empresa_id = self.get_selected_empresa_id()
        print(empresa_id)
        if empresa_id is None:
            self.app.notify("Selecione uma empresa para editar.", severity="error")
            return
        empresa = relatorios.fetch_one(self.conn, "SELECT * FROM empresa WHERE id = ?", (empresa_id,))
        if empresa:
            self.app.push_screen(EmpresaFormScreen(self.conn, existing=empresa))

    def action_excluir_empresa(self) -> None:
        empresa_id = self.get_selected_empresa_id()
        if empresa_id is None:
            self.app.notify("Selecione uma empresa para excluir.", severity="error")
            return

        def confirm_delete() -> None:
            try:
                self.conn.execute("DELETE FROM empresa WHERE id = ?", (empresa_id,))
                self.conn.commit()
                self.load_empresas()
                self.app.notify("Empresa excluída com sucesso!")
            except sqlite3.DatabaseError as exc:
                self.conn.rollback()
                self.app.notify(f"Erro ao excluir: {exc}", severity="error")

        self.app.push_screen(
            ConfirmDialog(
                title="Confirmar exclusão",
                message="Tem certeza que deseja excluir esse registro?",
                on_confirm=confirm_delete,
            )
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn_novo":
            self.action_nova_empresa()
        elif event.button.id == "btn_editar":
            self.action_editar_empresa()
        elif event.button.id == "btn_excluir":
            self.action_excluir_empresa()


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
        
        rows = relatorios.fetch_all(self.conn, "SELECT codigo, descricao, tipo, natureza FROM plano_contas ORDER BY codigo")
        for row in rows:
            table.add_row(row["codigo"], row["descricao"], row["tipo"], row["natureza"])

    def action_nova_conta(self) -> None:
        self.app.push_screen(ContaFormScreen(self.conn))

    def action_editar(self) -> None:
        table = self.query_one(DataTable)
        if table.cursor_row is not None:
            codigo = table.get_cell(table.cursor_row, 0)
            conta = relatorios.fetch_one(self.conn, "SELECT * FROM plano_contas WHERE codigo = ?", (codigo,))
            if conta:
                self.app.push_screen(ContaFormScreen(self.conn, existing=conta))

class LivroDiarioScreen(Screen):
    """Screen for displaying Livro Diário."""
    
    BINDINGS = [
        Binding("escape", "app.pop_screen", "Voltar"),
        Binding("n", "novo_lancamento", "Novo"),
        Binding("e", "editar_lancamento", "Editar"),
        Binding("d", "excluir_lancamento", "Excluir"),
    ]

    def __init__(self, conn: sqlite3.Connection, **kwargs):
        super().__init__(**kwargs)
        self.conn = conn

    def compose(self) -> ComposeResult:
        yield Header()
        yield DataTable(id="lancamento_table")
        with Horizontal():
            yield Button("Novo", id="btn_novo", variant="primary")
            yield Button("Editar", id="btn_editar")
            yield Button("Excluir", id="btn_excluir", variant="error")
        yield Footer()

    def on_mount(self) -> None:
        self.load_lancamentos()

    def load_lancamentos(self) -> None:
        table = self.query_one("#lancamento_table", DataTable)
        table.clear()
        table.add_columns("ID", "Data", "Histórico")
        table.cursor_type = "row"

        if EMPRESA_ATUAL is None:
            return

        rows = relatorios.fetch_all(
            self.conn,
            """
            SELECT id, data, historico
            FROM lancamento
            WHERE empresa_id = ?
            ORDER BY data, id
            """,
            (EMPRESA_ATUAL["id"],),
        )

        for row in rows:
            table.add_row(str(row["id"]), relatorios.display_date(row["data"]), row["historico"] or "")

    def get_selected_lancamento_id(self) -> Optional[int]:
        table = self.query_one("#lancamento_table", DataTable)
        if table.cursor_row is None:
            return None
        selected_id = table.get_cell(table.cursor_row, 0)
        try:
            return int(selected_id)
        except (TypeError, ValueError):
            return None

    def action_novo_lancamento(self) -> None:
        if EMPRESA_ATUAL is None:
            self.app.notify("Selecione uma empresa antes de lançar.", severity="error")
            return
        self.app.push_screen(LancamentoEditScreen(self.conn), self._on_edit_closed)

    def action_editar_lancamento(self) -> None:
        if EMPRESA_ATUAL is None:
            self.app.notify("Selecione uma empresa antes de editar.", severity="error")
            return

        lancamento_id = self.get_selected_lancamento_id()
        if lancamento_id is None:
            self.app.notify("Selecione um lançamento para editar.", severity="error")
            return

        self.app.push_screen(LancamentoEditScreen(self.conn, lancamento_id=lancamento_id), self._on_edit_closed)

    def action_excluir_lancamento(self) -> None:
        lancamento_id = self.get_selected_lancamento_id()
        if lancamento_id is None:
            self.app.notify("Selecione um lançamento para excluir.", severity="error")
            return

        def confirm_delete() -> None:
            try:
                self.conn.execute("DELETE FROM lancamento WHERE id = ?", (lancamento_id,))
                self.conn.commit()
                self.load_lancamentos()
                self.app.notify("Lançamento excluído com sucesso!")
            except sqlite3.DatabaseError as exc:
                self.conn.rollback()
                self.app.notify(f"Erro ao excluir lançamento: {exc}", severity="error")

        self.app.push_screen(
            ConfirmDialog(
                title="Confirmar exclusão",
                message="Deseja realmente excluir este lançamento?",
                on_confirm=confirm_delete,
            )
        )

    def _on_edit_closed(self, saved: Optional[bool]) -> None:
        if saved:
            self.load_lancamentos()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn_novo":
            self.action_novo_lancamento()
        elif event.button.id == "btn_editar":
            self.action_editar_lancamento()
        elif event.button.id == "btn_excluir":
            self.action_excluir_lancamento()


class LancamentoEditScreen(Screen):
    """Screen for creating or editing lançamento and its items."""

    BINDINGS = [
        Binding("escape", "app.pop_screen", "Voltar"),
        Binding("ctrl+s", "salvar_lancamento", "Salvar"),
    ]

    def __init__(self, conn: sqlite3.Connection, lancamento_id: Optional[int] = None, **kwargs):
        super().__init__(**kwargs)
        self.conn = conn
        self.lancamento_id = lancamento_id
        self.items: list[dict[str, Any]] = []

    def compose(self) -> ComposeResult:
        yield Header()
        with Container():
            yield Label("Data do Lançamento")
            yield Input(value=datetime.now().strftime("%d/%m/%Y"), id="lanc_data", placeholder="DD/MM/AAAA")
            yield Label("Histórico")
            yield Input(id="lanc_historico", placeholder="Histórico do lançamento")

            yield Label("Conta (ID, código ou nome)")
            yield Input(id="item_conta", placeholder="Ex.: 10, 1.1.1 ou Caixa")

            yield Label("Tipo de Lançamento")
            yield Select(
                [("Débito", "D"), ("Crédito", "C")],
                value="D",
                id="item_tipo",
            )

            yield Label("Valor")
            yield Input(id="item_valor", placeholder="0,00")

            with Horizontal(id="lancamento_item_actions"):
                yield Button("Incluir", id="btn_item_incluir", variant="primary")
                yield Button("Excluir", id="btn_item_excluir", variant="error")
                yield Button("Salvar Lançamento", id="btn_lanc_salvar", variant="success")

            yield DataTable(id="lancamento_item_table")
        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one("#lancamento_item_table", DataTable)
        table.add_columns("Código", "Nome Conta", "Tipo", "Valor")
        table.cursor_type = "row"

        if self.lancamento_id is not None:
            self._load_existing_lancamento()

    def _load_existing_lancamento(self) -> None:
        if EMPRESA_ATUAL is None:
            return

        lanc = relatorios.fetch_one(
            self.conn,
            """
            SELECT id, data, historico
            FROM lancamento
            WHERE id = ? AND empresa_id = ?
            """,
            (self.lancamento_id, EMPRESA_ATUAL["id"]),
        )
        if not lanc:
            self.app.notify("Lançamento não encontrado para a empresa selecionada.", severity="error")
            self.app.pop_screen()
            return

        self.query_one("#lanc_data", Input).value = relatorios.display_date(lanc["data"])
        self.query_one("#lanc_historico", Input).value = lanc["historico"] or ""

        rows = relatorios.fetch_all(
            self.conn,
            """
            SELECT li.conta_id, li.tipo, li.valor, c.codigo, c.descricao
            FROM lancamento_item li
            JOIN plano_contas c ON c.id = li.conta_id
            WHERE li.lancamento_id = ?
            ORDER BY li.id
            """,
            (self.lancamento_id,),
        )

        self.items = [
            {
                "conta_id": row["conta_id"],
                "codigo": row["codigo"],
                "descricao": row["descricao"],
                "tipo": row["tipo"],
                "valor": float(row["valor"]),
            }
            for row in rows
        ]
        self._refresh_items_table()

    def _find_account(self, raw_search: str) -> Optional[sqlite3.Row]:
        if EMPRESA_ATUAL is None:
            return None

        text = raw_search.strip()
        if not text:
            return None

        if text.isdigit():
            account = relatorios.fetch_one(
                self.conn,
                """
                SELECT id, codigo, descricao
                FROM plano_contas
                WHERE empresa_id = ? AND aceita_lancamento = 1 AND id = ?
                """,
                (EMPRESA_ATUAL["id"], int(text)),
            )
            if account:
                return account

        return relatorios.fetch_one(
            self.conn,
            """
            SELECT id, codigo, descricao
            FROM plano_contas
            WHERE empresa_id = ?
              AND aceita_lancamento = 1
              AND (codigo = ? OR UPPER(descricao) = UPPER(?) OR UPPER(descricao) LIKE UPPER(?))
            ORDER BY CASE
                WHEN codigo = ? THEN 0
                WHEN UPPER(descricao) = UPPER(?) THEN 1
                ELSE 2
            END,
            codigo
            LIMIT 1
            """,
            (EMPRESA_ATUAL["id"], text, text, f"%{text}%", text, text),
        )

    def _refresh_items_table(self) -> None:
        table = self.query_one("#lancamento_item_table", DataTable)
        table.clear()
        for item in self.items:
            table.add_row(
                item["codigo"],
                item["descricao"],
                item["tipo"],
                relatorios.format_currency(item["valor"]),
            )

    def _incluir_item(self) -> None:
        if EMPRESA_ATUAL is None:
            self.app.notify("Selecione uma empresa antes de incluir itens.", severity="error")
            return

        conta_raw = self.query_one("#item_conta", Input).value.strip()
        if not conta_raw:
            self.app.notify("Informe ID, código ou nome da conta.", severity="error")
            return

        conta = self._find_account(conta_raw)
        if not conta:
            self.app.notify("Conta não encontrada para a empresa atual.", severity="error")
            return

        tipo = self.query_one("#item_tipo", Select).value
        if tipo not in ("D", "C"):
            self.app.notify("Selecione Débito ou Crédito.", severity="error")
            return

        valor_raw = self.query_one("#item_valor", Input).value
        try:
            valor = relatorios.parse_decimal(valor_raw)
        except ValueError as exc:
            self.app.notify(str(exc), severity="error")
            return

        self.items.append(
            {
                "conta_id": int(conta["id"]),
                "codigo": conta["codigo"],
                "descricao": conta["descricao"],
                "tipo": tipo,
                "valor": valor,
            }
        )
        self._refresh_items_table()

        self.query_one("#item_conta", Input).value = ""
        self.query_one("#item_valor", Input).value = ""
        self.app.notify("Item incluído com sucesso!")

    def _excluir_item(self) -> None:
        table = self.query_one("#lancamento_item_table", DataTable)
        if table.cursor_row is None:
            self.app.notify("Selecione um item para excluir.", severity="error")
            return

        index = table.cursor_row
        if index < 0 or index >= len(self.items):
            self.app.notify("Item selecionado é inválido.", severity="error")
            return

        self.items.pop(index)
        self._refresh_items_table()
        self.app.notify("Item excluído.")

    def action_salvar_lancamento(self) -> None:
        self._salvar_lancamento()

    def _salvar_lancamento(self) -> None:
        if EMPRESA_ATUAL is None:
            self.app.notify("Selecione uma empresa antes de salvar.", severity="error")
            return

        if not self.items:
            self.app.notify("Inclua pelo menos um item no lançamento.", severity="error")
            return

        data_input = self.query_one("#lanc_data", Input).value.strip()
        historico = self.query_one("#lanc_historico", Input).value.strip()
        if not historico:
            self.app.notify("Informe o histórico do lançamento.", severity="error")
            return

        try:
            data_norm = relatorios.normalize_date(data_input)
        except ValueError as exc:
            self.app.notify(str(exc), severity="error")
            return

        try:
            if self.lancamento_id is None:
                cursor = self.conn.execute(
                    """
                    INSERT INTO lancamento (empresa_id, data, historico)
                    VALUES (?, ?, ?)
                    """,
                    (EMPRESA_ATUAL["id"], data_norm, historico),
                )
                lancamento_id = cursor.lastrowid
            else:
                lancamento_id = self.lancamento_id
                self.conn.execute(
                    """
                    UPDATE lancamento
                    SET data = ?, historico = ?, empresa_id = ?
                    WHERE id = ?
                    """,
                    (data_norm, historico, EMPRESA_ATUAL["id"], lancamento_id),
                )
                self.conn.execute("DELETE FROM lancamento_item WHERE lancamento_id = ?", (lancamento_id,))

            for item in self.items:
                self.conn.execute(
                    """
                    INSERT INTO lancamento_item (lancamento_id, conta_id, tipo, valor)
                    VALUES (?, ?, ?, ?)
                    """,
                    (lancamento_id, item["conta_id"], item["tipo"], item["valor"]),
                )

            self.conn.commit()
            self.app.notify("Lançamento salvo com sucesso!")
            self.dismiss(True)
        except sqlite3.DatabaseError as exc:
            self.conn.rollback()
            self.app.notify(f"Erro ao salvar lançamento: {exc}", severity="error")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn_item_incluir":
            self._incluir_item()
        elif event.button.id == "btn_item_excluir":
            self._excluir_item()
        elif event.button.id == "btn_lanc_salvar":
            self._salvar_lancamento()

class RelatoriosScreen(Screen):
    """Screen for displaying Relatórios."""
    
    BINDINGS = [
        Binding("escape", "app.pop_screen", "Voltar"),
    ]

    def __init__(self, conn: sqlite3.Connection, **kwargs):
        super().__init__(**kwargs)
        self.conn = conn

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label("Relatórios - Em construção...")
        yield Footer()    

class SetEmpresaScreen(Screen):
    """Screen for setting current empresa."""
    
    BINDINGS = [
        Binding("escape", "app.pop_screen", "Voltar"),
        Binding("ctrl+s", "definir_empresa", "Definir"),
    ]

    def __init__(self, conn: sqlite3.Connection, **kwargs):
        super().__init__(**kwargs)
        self.conn = conn

    def compose(self) -> ComposeResult:
        yield Header()
        with Container():
            yield Label("Definir Empresa Atual", id="set_empresa_title")
            yield Label("Informe o ID da empresa:")
            yield Input(placeholder="Ex.: 1", id="empresa_id_input")
            with Horizontal():
                yield Button("Definir", id="btn_definir", variant="primary")
                yield Button("Cancelar", id="btn_cancelar")
        yield Footer()            

    def action_definir_empresa(self) -> None:
        self._definir_empresa_atual()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn_definir":
            self._definir_empresa_atual()
        elif event.button.id == "btn_cancelar":
            self.app.pop_screen()

    def _definir_empresa_atual(self) -> None:
        global EMPRESA_ATUAL

        empresa_id_text = self.query_one("#empresa_id_input", Input).value.strip()
        if not empresa_id_text:
            self.app.notify("Informe o ID da empresa.", severity="error")
            return

        try:
            empresa_id = int(empresa_id_text)
        except ValueError:
            self.app.notify("ID da empresa deve ser um número inteiro.", severity="error")
            return

        empresa = relatorios.fetch_one(
            self.conn,
            "SELECT id, nome FROM empresa WHERE id = ?",
            (empresa_id,),
        )

        if not empresa:
            self.app.notify("Empresa não encontrada para o ID informado.", severity="error")
            return

        EMPRESA_ATUAL = empresa
        self.app.notify(f"Empresa '{empresa['nome']}' definida com sucesso!")
        self.dismiss(empresa)

class MainScreen(Screen):
    """Main menu screen."""
    
    BINDINGS = [
        Binding("q", "quit", "Sair"),
        Binding("a", "livro_diario", "Livro Diário"),
        Binding("b", "relatorios", "Relatórios"),
        Binding("c", "cadastro_empresa", "Empresa"),
        Binding("d", "set_empresa", "Definir Empresa"),
        Binding("e", "plano_contas", "Contas"),
    ]

    def __init__(self, conn: sqlite3.Connection, **kwargs):
        super().__init__(**kwargs)
        self.conn = conn

    def compose(self) -> ComposeResult:
        yield Header()
        with Container():
            yield Label("PJLA Contabilidade OFFLINE", id="title")
            yield Label(self._empresa_info_text(), id="empresa_info")
        yield Footer()

    def _empresa_info_text(self) -> str:
        if EMPRESA_ATUAL is None:
            return "Selecione uma empresa"
        return f"Empresa: {EMPRESA_ATUAL['nome']}"

    def _refresh_empresa_info(self) -> None:
        empresa_info = self.query_one("#empresa_info", Label)
        empresa_info.update(self._empresa_info_text())

    def on_mount(self) -> None:
        self._refresh_empresa_info()

    def action_livro_diario(self) -> None:
        self.app.push_screen(LivroDiarioScreen(self.conn))

    def action_relatorios(self) -> None:
        self.app.push_screen(RelatoriosScreen(self.conn))

    def action_cadastro_empresa(self) -> None:
        self.app.push_screen(EmpresaListScreen(self.conn))

    def action_plano_contas(self) -> None:
        self.app.push_screen(ContaListScreen(self.conn))

    def action_set_empresa(self) -> None:
        self.app.push_screen(SetEmpresaScreen(self.conn), self._on_set_empresa_closed)

    def _on_set_empresa_closed(self, _result: Optional[sqlite3.Row]) -> None:
        self._refresh_empresa_info()


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

    #lancamento_item_actions {
        width: 100%;
        align: center middle;
        margin: 1 0;
    }
    """

    def __init__(self):
        super().__init__()
        self.conn = relatorios.connect_db()

    def on_mount(self) -> None:
        self.push_screen(MainScreen(self.conn))

    def on_unmount(self) -> None:
        self.conn.close()


if __name__ == "__main__":
    app = ContabilidadeApp()
    app.run()
