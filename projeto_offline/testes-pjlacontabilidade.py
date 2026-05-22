"""Testes focados para operações de lançamentos da aplicação principal."""

import sqlite3
import sys

import pjlacontabilidade as app


def setup_db():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.executescript(
        """
        CREATE TABLE empresa (
            id INTEGER PRIMARY KEY,
            cnpj TEXT NOT NULL,
            nome TEXT NOT NULL
        );

        CREATE TABLE plano_contas (
            id INTEGER PRIMARY KEY,
            empresa_id INTEGER,
            codigo TEXT NOT NULL,
            descricao TEXT NOT NULL,
            tipo TEXT NOT NULL,
            natureza TEXT,
            nivel INTEGER NOT NULL,
            aceita_lancamento INTEGER DEFAULT 1
        );

        CREATE TABLE lancamento (
            id INTEGER PRIMARY KEY,
            empresa_id INTEGER,
            data TEXT NOT NULL,
            numero TEXT,
            historico TEXT
        );

        CREATE TABLE lancamento_item (
            id INTEGER PRIMARY KEY,
            lancamento_id INTEGER,
            conta_id INTEGER,
            tipo TEXT NOT NULL,
            valor REAL NOT NULL
        );
        """
    )

    conn.execute("INSERT INTO empresa (id, cnpj, nome) VALUES (1, '00.000.000/0001-00', 'Empresa Teste')")
    conn.execute(
        "INSERT INTO plano_contas (id, empresa_id, codigo, descricao, tipo, natureza, nivel, aceita_lancamento) VALUES (1, 1, '1.1.1', 'Caixa', 'A', 'D', 3, 1)"
    )
    conn.execute(
        "INSERT INTO plano_contas (id, empresa_id, codigo, descricao, tipo, natureza, nivel, aceita_lancamento) VALUES (2, 1, '2.1.1', 'Receita', 'A', 'C', 3, 1)"
    )
    conn.execute(
        "INSERT INTO plano_contas (id, empresa_id, codigo, descricao, tipo, natureza, nivel, aceita_lancamento) VALUES (3, 1, '1.1.2', 'Banco', 'A', 'D', 3, 1)"
    )
    conn.execute(
        "INSERT INTO lancamento (id, empresa_id, data, numero, historico) VALUES (1, 1, '2024-01-10', 'DOC1', 'Venda inicial')"
    )
    conn.execute(
        "INSERT INTO lancamento_item (id, lancamento_id, conta_id, tipo, valor) VALUES (1, 1, 1, 'D', 100.0)"
    )
    conn.execute(
        "INSERT INTO lancamento_item (id, lancamento_id, conta_id, tipo, valor) VALUES (2, 1, 2, 'C', 100.0)"
    )
    conn.commit()
    return conn


def test_replace_lancamento():
    conn = setup_db()
    header = {"data": "2024-02-05", "numero": "DOC2", "historico": "Venda corrigida"}
    items = [
        {"conta_id": 3, "tipo": "D", "valor": 150.0, "historico": "Venda corrigida"},
        {"conta_id": 2, "tipo": "C", "valor": 150.0, "historico": "Venda corrigida"},
    ]

    conn.execute("BEGIN")
    app.replace_lancamento(conn, 1, 1, header, items)
    conn.commit()

    lancamento = app.fetch_lancamento(conn, 1, 1)
    fetched_items = app.fetch_lancamento_items(conn, 1)

    assert lancamento is not None
    assert lancamento["data"] == "2024-02-05"
    assert lancamento["numero"] == "DOC2"
    assert lancamento["historico"] == "Venda corrigida"
    assert len(fetched_items) == 2
    assert fetched_items[0]["conta_id"] == 3
    assert fetched_items[1]["conta_id"] == 2


def test_delete_lancamento():
    conn = setup_db()

    conn.execute("BEGIN")
    app.delete_lancamento(conn, 1, 1)
    conn.commit()

    lancamento = app.fetch_lancamento(conn, 1, 1)
    fetched_items = app.fetch_lancamento_items(conn, 1)

    assert lancamento is None
    assert fetched_items == []


if __name__ == "__main__":
    try:
        test_replace_lancamento()
        test_delete_lancamento()
    except AssertionError as exc:
        print("Teste falhou:", exc)
        sys.exit(2)
    except Exception as exc:
        print("Erro durante testes:", exc)
        sys.exit(1)
    else:
        print("SUCESSO: testes de pjlacontabilidade passaram")