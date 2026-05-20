from __future__ import annotations

import sqlite3
from typing import Optional

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Container
from textual.screen import Screen
from textual.widgets import Footer, Header, Label

import experiencia02_tela_estado as estado
from experiencia02_tela_app import run_app
from experiencia02_tela_assinaturas_digitais import AssinaturaDigitalListScreen
from experiencia02_tela_centro_custos import CentroCustoListScreen
from experiencia02_tela_certificados_digitais import CertificadoDigitalListScreen
from experiencia02_tela_contas import ContaListScreen
from experiencia02_tela_empresa import EmpresaListScreen
from experiencia02_tela_livro_diario import LivroDiarioScreen
from experiencia02_tela_plano_referencial import PlanoReferencialListScreen
from experiencia02_tela_relatorios import RelatoriosScreen
from experiencia02_tela_set_empresa import SetEmpresaScreen
from experiencia02_tela_tags import TagListScreen
from experiencia02_tela_usuarios import UsuarioListScreen


class MainScreen(Screen):
    """Main menu screen."""

    BINDINGS = [
        Binding("q", "quit", "Sair"),
        Binding("a", "livro_diario", "Livro Diário"),
        Binding("b", "relatorios", "Relatórios"),
        Binding("c", "cadastro_empresa", "Empresa"),
        Binding("d", "set_empresa", "Definir Empresa"),
        Binding("e", "plano_contas", "Contas"),
        Binding("f", "plano_referencial", "Plano Referencial"),
        Binding("g", "usuarios", "Usuários"),
        Binding("h", "centro_custos", "Centro de Custos"),
        Binding("i", "tags", "Tags"),
        Binding("j", "certificados_digitais", "Certificados Digitais"),
        Binding("k", "assinaturas_digitais", "Assinaturas Digitais"),
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
        if estado.EMPRESA_ATUAL is None:
            return "Selecione uma empresa"
        return f"Empresa: {estado.EMPRESA_ATUAL['nome']}"

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

    def action_plano_referencial(self) -> None:
        self.app.push_screen(PlanoReferencialListScreen(self.conn))

    def action_usuarios(self) -> None:
        self.app.push_screen(UsuarioListScreen(self.conn))

    def action_centro_custos(self) -> None:
        self.app.push_screen(CentroCustoListScreen(self.conn))

    def action_tags(self) -> None:
        self.app.push_screen(TagListScreen(self.conn))

    def action_certificados_digitais(self) -> None:
        self.app.push_screen(CertificadoDigitalListScreen(self.conn))

    def action_assinaturas_digitais(self) -> None:
        self.app.push_screen(AssinaturaDigitalListScreen(self.conn))

    def action_set_empresa(self) -> None:
        self.app.push_screen(SetEmpresaScreen(self.conn), self._on_set_empresa_closed)

    def _on_set_empresa_closed(self, _result: Optional[sqlite3.Row]) -> None:
        self._refresh_empresa_info()


if __name__ == "__main__":
    run_app(MainScreen)
