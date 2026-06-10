import sqlite3
from utils import *

def menu_mapa_demontracoes(conn: sqlite3.Connection) -> None:
    print("\n------\n")
    print("MAPA DE DEMONSTRAÇÕES CONTÁBEIS")
    empresa = ask_empresa(conn)
    if not empresa:
        pause("Empresa não encontrada. Clique ENTER para voltar ao menu principal.")
        return
    while True:
        print("\n[a] Criar Mapa de Demonstrações Contábeis")
        print("[b] Visualizar Mapas de Demonstrações Contábeis")
        print("[c] Excluir Mapa de Demonstrações Contábeis")
        print("[d] Gerar Relatório de Mapa de Demonstrações Contábeis")
        print("[q] Voltar")
        choice = input("\nEscolha: ").strip().lower()
        if choice == "a":
            criar_mapa(conn)
        elif choice == "b":
            visualizar_mapas(conn, empresa)
        elif choice == "c":
            excluir_mapa(conn, empresa)
        elif choice == 'd':  
            gerar_relatorio_mapa(conn, empresa)
        elif choice == "q":
            return
        else:
            pause("Opção inválida. Clique ENTER para tentar novamente.")


def criar_mapa(conn: sqlite3.Connection) -> None:
    print("\nCriar Mapa de Demonstrações Contábeis")
    print("-" * 20)
    while True:
        conta_id = input("ID da Conta (plano_contas) [? para listar]: ").strip()
        if conta_id == "?":
            rows = fetch_all(conn, "SELECT id, codigo, descricao FROM plano_contas WHERE excluido_at IS NULL ORDER BY codigo")
            if not rows:
                print("Nenhuma conta encontrada.")
            else:
                print(f"\n{'ID':<6} {'CÓDIGO':<12} {'DESCRIÇÃO'}")
                print("-" * 50)
                for row in rows:
                    print(f"{row['id']:<6} {row['codigo']:<12} {row['descricao']}")
                print()
            continue
        if not conta_id.isdigit():
            pause("ID da conta inválido.")
            return
        break
    print("Tipo: [1] DRE  [2] DVA  [3] DFC")
    tipo_opcoes = {"1": "DRE", "2": "DVA", "3": "DFC"}
    tipo_escolha = input("Tipo: ").strip()
    tipo = tipo_opcoes.get(tipo_escolha)
    if not tipo:
        pause("Tipo inválido.")
        return
    categoria = input("Categoria: ").strip()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO mapa_demonstracoes (conta_id, tipo, categoria) VALUES (?, ?, ?)",
        (int(conta_id), tipo, categoria),
    )
    conn.commit()
    pause("Mapa de Demonstrações Contábeis criado com sucesso.")

def visualizar_mapas(conn: sqlite3.Connection, empresa: dict) -> None:
    rows = fetch_all(conn, """
        SELECT m.id, m.tipo, m.categoria, c.codigo AS conta_codigo, c.descricao AS conta_descricao
        FROM mapa_demonstracoes m
        JOIN plano_contas c ON m.conta_id = c.id
        WHERE c.empresa_id = ? AND c.excluido_at IS NULL
        ORDER BY m.id
    """, (empresa['id'],))
    if not rows:
        pause("Nenhum mapa de demonstrações contábeis encontrado.")
        return

    print(f"\n{'ID':<6} {'TIPO':<6} {'CATEGORIA':<20} {'CONTA CÓDIGO':<12} {'CONTA DESCRIÇÃO'}")
    print("-" * 80)
    for row in rows:
        print(f"{row['id']:<6} {row['tipo']:<6} {row['categoria']:<20} {row['conta_codigo']:<12} {row['conta_descricao']}")
    pause("Clique ENTER para voltar ao submenu.")

def excluir_mapa(conn: sqlite3.Connection, empresa: dict) -> None:
    mapa_id = input("ID do Mapa de Demonstrações Contábeis a excluir: ").strip()
    if not mapa_id.isdigit():
        pause("ID inválido.")
        return
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM mapa_demonstracoes
        WHERE id = ? AND conta_id IN (SELECT id FROM plano_contas WHERE empresa_id = ?)
    """, (int(mapa_id), empresa['id']))
    if cursor.rowcount == 0:
        pause("Mapa de Demonstrações Contábeis não encontrado ou não pertence à empresa.")
    else:
        conn.commit()
        pause("Mapa de Demonstrações Contábeis excluído com sucesso.")

def gerar_relatorio_mapa(conn: sqlite3.Connection, empresa: dict) -> None:
    print("\nGerar Relatório de Mapa de Demonstrações Contábeis")
    print("-" * 40)
    tipo = input("Tipo (DRE, DVA, DFC): ").strip().upper()
    if tipo not in ["DRE", "DVA", "DFC"]:
        pause("Tipo inválido.")
        return
    categoria = input("Categoria: ").strip()
    mes_str = input("Qual mês deseja extrair o relatório? (1-12): ").strip()
    if not mes_str.isdigit() or not (1 <= int(mes_str) <= 12):
        pause("Mês inválido.")
        return
    mes = int(mes_str)
    rows = fetch_all(conn, """
        SELECT
            m.id,
            m.tipo,
            m.categoria,
            c.codigo AS conta_codigo,
            c.descricao AS conta_descricao,
            COALESCE(SUM(CASE WHEN li.tipo = 'D' THEN li.valor ELSE 0 END), 0) -
            COALESCE(SUM(CASE WHEN li.tipo = 'C' THEN li.valor ELSE 0 END), 0) AS saldo
        FROM mapa_demonstracoes m
        JOIN plano_contas c ON m.conta_id = c.id
        LEFT JOIN lancamento_item li
            ON li.conta_id = c.id
            AND li.excluido_at IS NULL
        LEFT JOIN lancamento l
            ON l.id = li.lancamento_id
            AND l.empresa_id = ?
            AND CAST(strftime('%m', l.data) AS INTEGER) = ?
            AND l.excluido_at IS NULL
        WHERE c.empresa_id = ?
          AND c.excluido_at IS NULL
          AND m.tipo = ?
          AND m.categoria = ?
          AND m.excluido_at IS NULL
        GROUP BY m.id, m.tipo, m.categoria, c.codigo, c.descricao
        ORDER BY c.codigo
    """, (empresa['id'], mes, empresa['id'], tipo, categoria))
    if not rows:
        pause("Nenhum mapa de demonstrações contábeis encontrado para os critérios informados.")
        return

    print(f"\n{'ID':<6} {'TIPO':<6} {'CATEGORIA':<20} {'CONTA CÓDIGO':<12} {'CONTA DESCRIÇÃO':<30} {'SALDO':>12}")
    print("-" * 95)
    for row in rows:
        print(f"{row['id']:<6} {row['tipo']:<6} {row['categoria']:<20} {row['conta_codigo']:<12} {row['conta_descricao']:<30} {row['saldo']:>12.2f}")
    pause("Clique ENTER para voltar ao submenu.")

