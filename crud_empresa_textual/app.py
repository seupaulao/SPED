from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal, Vertical
from textual.screen import ModalScreen, Screen
from textual.widgets import Button, DataTable, Footer, Header, Input, Label, Static

import database


# ---------------------------------------------------------------------------
# Modal de confirmação de exclusão
# ---------------------------------------------------------------------------

class ConfirmDeleteModal(ModalScreen[bool]):
    """Modal que pede confirmação antes de excluir uma empresa."""

    DEFAULT_CSS = """
    ConfirmDeleteModal {
        align: center middle;
    }
    ConfirmDeleteModal > Vertical {
        background: $surface;
        border: thick $error;
        padding: 1 2;
        width: 60;
        height: auto;
    }
    ConfirmDeleteModal #msg {
        text-align: center;
        margin-bottom: 1;
    }
    ConfirmDeleteModal Horizontal {
        align: center middle;
        height: auto;
        margin-top: 1;
    }
    ConfirmDeleteModal Button {
        margin: 0 1;
    }
    """

    def __init__(self, empresa_nome: str, empresa_cnpj: str) -> None:
        super().__init__()
        self.empresa_nome = empresa_nome
        self.empresa_cnpj = empresa_cnpj

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Static("⚠  Confirmar Exclusão", id="title")
            yield Static(
                f"Deseja excluir a empresa?\n\n"
                f"  Nome: {self.empresa_nome}\n"
                f"  CNPJ: {self.empresa_cnpj}",
                id="msg",
            )
            with Horizontal():
                yield Button("Confirmar", variant="error", id="btn-confirmar")
                yield Button("Cancelar", variant="default", id="btn-cancelar")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.dismiss(event.button.id == "btn-confirmar")


# ---------------------------------------------------------------------------
# Tela de formulário (criação e edição)
# ---------------------------------------------------------------------------

class EmpresaFormScreen(Screen):
    """Formulário para criar ou editar uma empresa."""

    DEFAULT_CSS = """
    EmpresaFormScreen {
        align: center middle;
    }
    EmpresaFormScreen > Vertical {
        background: $surface;
        border: thick $primary;
        padding: 1 2;
        width: 70;
        height: auto;
    }
    EmpresaFormScreen #form-title {
        text-style: bold;
        margin-bottom: 1;
    }
    EmpresaFormScreen Label {
        margin-top: 1;
    }
    EmpresaFormScreen Input {
        margin-top: 0;
    }
    EmpresaFormScreen #error-msg {
        color: $error;
        margin-top: 1;
        height: 1;
    }
    EmpresaFormScreen Horizontal {
        align: center middle;
        height: auto;
        margin-top: 2;
    }
    EmpresaFormScreen Button {
        margin: 0 1;
    }
    """

    def __init__(
        self,
        empresa_id: int | None = None,
        cnpj: str = "",
        nome: str = "",
    ) -> None:
        super().__init__()
        self.empresa_id = empresa_id
        self._cnpj = cnpj
        self._nome = nome
        self._is_edit = empresa_id is not None

    def compose(self) -> ComposeResult:
        titulo = "Editar Empresa" if self._is_edit else "Nova Empresa"
        with Vertical():
            yield Static(titulo, id="form-title")
            yield Label("CNPJ")
            yield Input(
                value=self._cnpj,
                placeholder="00.000.000/0000-00",
                id="input-cnpj",
            )
            yield Label("Nome")
            yield Input(value=self._nome, placeholder="Razão social", id="input-nome")
            yield Static("", id="error-msg")
            with Horizontal():
                yield Button("Salvar", variant="primary", id="btn-salvar")
                yield Button("Cancelar", variant="default", id="btn-cancelar")

    def _validate(self) -> str | None:
        """Retorna mensagem de erro ou None se válido."""
        cnpj = self.query_one("#input-cnpj", Input).value.strip()
        nome = self.query_one("#input-nome", Input).value.strip()
        if not cnpj:
            return "CNPJ é obrigatório."
        if not nome:
            return "Nome é obrigatório."
        return None

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        error_label = self.query_one("#error-msg", Static)

        if event.button.id == "btn-cancelar":
            await self.dismiss(False)
            return

        error = self._validate()
        if error:
            error_label.update(error)
            return

        cnpj = self.query_one("#input-cnpj", Input).value.strip()
        nome = self.query_one("#input-nome", Input).value.strip()

        try:
            if self._is_edit:
                database.update(self.empresa_id, cnpj, nome)
            else:
                database.create(cnpj, nome)
        except Exception as exc:
            error_label.update(f"Erro: {exc}")
            return

        self.dismiss(True)


# ---------------------------------------------------------------------------
# Tela principal
# ---------------------------------------------------------------------------

class MainScreen(Screen):
    """Tela principal: listagem de empresas com ações CRUD."""

    BINDINGS = [
        Binding("n", "novo", "Novo"),
        Binding("e", "editar", "Editar"),
        Binding("delete", "excluir", "Excluir"),
    ]

    DEFAULT_CSS = """
    MainScreen {
        layout: vertical;
    }
    #table-container {
        height: 1fr;
        border: solid $primary;
        margin: 1 1 0 1;
    }
    #btn-bar {
        height: auto;
        margin: 1;
        align: left middle;
    }
    #btn-bar Button {
        margin-right: 1;
    }
    """

    def __init__(self) -> None:
        super().__init__()
        self._selected_row_key: str | None = None
        self._selected_empresa: dict | None = None

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Container(id="table-container"):
            table = DataTable(id="empresa-table", cursor_type="row")
            yield table
        with Horizontal(id="btn-bar"):
            yield Button("➕ Novo", variant="success", id="btn-novo")
            yield Button("✏  Editar", variant="primary", id="btn-editar", disabled=True)
            yield Button("🗑  Excluir", variant="error", id="btn-excluir", disabled=True)
        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one("#empresa-table", DataTable)
        table.add_columns("ID", "CNPJ", "Nome")
        self.refresh_table()

    def refresh_table(self) -> None:
        table = self.query_one("#empresa-table", DataTable)
        table.clear()
        for row in database.get_all():
            table.add_row(str(row["id"]), row["cnpj"], row["nome"], key=str(row["id"]))
        # Limpa seleção ao atualizar
        self._selected_row_key = None
        self._selected_empresa = None
        self._update_buttons()

    def _update_buttons(self) -> None:
        has_selection = self._selected_empresa is not None
        self.query_one("#btn-editar", Button).disabled = not has_selection
        self.query_one("#btn-excluir", Button).disabled = not has_selection

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        self._selected_row_key = event.row_key.value
        table = self.query_one("#empresa-table", DataTable)
        row_data = table.get_row(event.row_key)
        self._selected_empresa = {
            "id": int(row_data[0]),
            "cnpj": row_data[1],
            "nome": row_data[2],
        }
        self._update_buttons()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-novo":
            self.action_novo()
        elif event.button.id == "btn-editar":
            self.action_editar()
        elif event.button.id == "btn-excluir":
            self.action_excluir()

    def action_novo(self) -> None:
        self.app.push_screen(EmpresaFormScreen(), self._on_form_closed)

    def action_editar(self) -> None:
        if not self._selected_empresa:
            return
        self.app.push_screen(
            EmpresaFormScreen(
                empresa_id=self._selected_empresa["id"],
                cnpj=self._selected_empresa["cnpj"],
                nome=self._selected_empresa["nome"],
            )
            ,
            self._on_form_closed,
        )

    def _on_form_closed(self, saved: bool | None) -> None:
        if saved:
            self.refresh_table()

    def action_excluir(self) -> None:
        if not self._selected_empresa:
            return

        def handle_confirm(confirmed: bool) -> None:
            if confirmed:
                database.delete(self._selected_empresa["id"])
                self.refresh_table()

        self.app.push_screen(
            ConfirmDeleteModal(
                empresa_nome=self._selected_empresa["nome"],
                empresa_cnpj=self._selected_empresa["cnpj"],
            ),
            handle_confirm,
        )


# ---------------------------------------------------------------------------
# Aplicação
# ---------------------------------------------------------------------------

class EmpresasApp(App):
    """Aplicação CRUD de Empresas."""

    TITLE = "Cadastro de Empresas"

    def on_mount(self) -> None:
        database.init_db()
        self.push_screen(MainScreen())


if __name__ == "__main__":
    EmpresasApp().run()
