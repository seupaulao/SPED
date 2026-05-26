from utils import *

## criar metodos para trabalhar com o PLANO DE CONTAS
def nova_conta(conn: sqlite3.Connection) -> None:
    empresa_id = input('Qual o Codigo da empresa? -> ')
    codigo = input('Qual o codigo da conta? Formato 01.01.01 -> ')
    descricao = input('Qual a descricao da conta? Formato TIPO:CONTA:SUBCONTA -> ')
    tipo = input('Conta eh [A]Analitica? Conta eh [S]intetica? -> ')
    natureza = input('Natureza da Conta eh [D]evedora ou [C]redora -> ') # D ou C
    grupo = input('Grupo da Conta? -> ')
    dre_grupo = input('Grupo DRE? -> ')
    subgrupo  = input('Subgrupo? -> ')
    fluxo_caixa_tipo  = input('Tipo Fluxo Caixa? -> ')
    nivel  = input('Nivel? -> ')
    conta_pai_id  = input('Conta PAI? -> ')
    codigo_referencial  = input('Codigo Referencial? -> ')
    aceita_lancamento = 1
#    created_at = input("Data da Criação da conta [DD/MM/AAAA]: ").strip()
    ## operacoes de banco
    try:
        conn.execute("BEGIN")
        cur = conn.cursor()
        cur.execute(
        """
        INSERT INTO plano_contas (empresa_id, codigo, descricao, tipo, natureza, grupo, dre_grupo, subgrupo, fluxo_caixa_tipo, nivel, conta_pai_id, codigo_referencial, aceita_lancamento)
        VALUES (?, ?, ?, ?, ? , ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (empresa_id, codigo, descricao, tipo, natureza, grupo, dre_grupo, subgrupo, fluxo_caixa_tipo, nivel, conta_pai_id, codigo_referencial, aceita_lancamento),
        )    
        conn.commit()
        print("Conta salva com sucesso.")
    except sqlite3.DatabaseError as exc:
        conn.rollback()
        pause(f"Erro ao salvar conta: {exc}. Clique ENTER para voltar ao submenu.")
        return    
    
def editar_conta(conn: sqlite3.Connection) -> None:
    codigo = input("Qual o código da conta que deseja editar? Digite '.' para voltar ao submenu: ").strip()
    if codigo == ".":
        return

    conta = fetch_one(conn, "SELECT * FROM plano_contas WHERE codigo = ?", (codigo,))
    if not conta:
        pause("Conta não encontrada. Clique ENTER para voltar ao submenu.")
        return

    print("\nConta encontrada:")
    print(f"Código: {conta['codigo']}")
    print(f"Descrição: {conta['descricao']}")
    print(f"Tipo: {conta['tipo']}")
    print(f"Natureza: {conta['natureza']}")

    descricao = input("Nova descrição (ou ENTER para manter): ").strip() or conta['descricao']
    tipo = input("Novo tipo [A/S] (ou ENTER para manter): ").strip().upper() or conta['tipo']
    natureza = input("Nova natureza [D/C] (ou ENTER para manter): ").strip().upper() or conta['natureza']

    try:
        conn.execute(
            """
            UPDATE plano_contas
            SET descricao = ?, tipo = ?, natureza = ?
            WHERE codigo = ?
            """,
            (descricao, tipo, natureza, codigo),
        )
        conn.commit()
        pause("Conta atualizada com sucesso. Clique ENTER para voltar ao submenu.")
    except sqlite3.DatabaseError as exc:
        conn.rollback()
        pause(f"Erro ao atualizar conta: {exc}. Clique ENTER para voltar ao submenu.")

def detalhar_conta(conn: sqlite3.Connection) -> None:
    codigo = input("Qual o código da conta que deseja detalhar? Digite '.' para voltar ao submenu: ").strip()
    if codigo == ".":
        return

    conta = fetch_one(conn, "SELECT * FROM plano_contas WHERE codigo = ?", (codigo,))
    if not conta:
        pause("Conta não encontrada. Clique ENTER para voltar ao submenu.")
        return

    print("\nDetalhes da conta:")
    print(f"Código: {conta['codigo']}")
    print(f"Descrição: {conta['descricao']}")
    print(f"Tipo: {conta['tipo']}")
    print(f"Natureza: {conta['natureza']}")
    print(f"Grupo: {conta['grupo']}")
    print(f"DRE Grupo: {conta['dre_grupo']}")
    print(f"Subgrupo: {conta['subgrupo']}")
    print(f"Fluxo Caixa Tipo: {conta['fluxo_caixa_tipo']}")
    print(f"Nível: {conta['nivel']}")
    print(f"Conta Pai ID: {conta['conta_pai_id']}")
    print(f"Código Referencial: {conta['codigo_referencial']}")
    print(f"Aceita Lançamento: {conta['aceita_lancamento']}")
    print(f"Criado em: {conta['created_at']}")
    pause("Clique ENTER para voltar ao submenu.")

def listar_contas(conn: sqlite3.Connection) -> None:
    rows = fetch_all(conn, "SELECT codigo, descricao, tipo, natureza FROM plano_contas ORDER BY codigo")
    if not rows:
        pause("Nenhuma conta encontrada. Clique ENTER para voltar ao submenu.")
        return

    print("\nCÓDIGO | DESCRIÇÃO | TIPO | NATUREZA")
    print("-" * 50)
    for row in rows:
        print(f"{row['codigo']:<10} | {row['descricao']:<20} | {row['tipo']:<4} | {row['natureza']:<8}")
    pause("Clique ENTER para voltar ao submenu.")

def listar_contas_empresa(conn: sqlite3.Connection, empresa: dict) -> None:
    rows = fetch_all(conn, "SELECT codigo, descricao, tipo, natureza FROM plano_contas WHERE empresa_id = ? ORDER BY codigo", (empresa['id'],))
    if not rows:
        pause("Nenhuma conta encontrada. Clique ENTER para voltar ao submenu.")
        return

    print("\nCÓDIGO | DESCRIÇÃO | TIPO | NATUREZA")
    print("-" * 50)
    for row in rows:
        print(f"{row['codigo']:<10} | {row['descricao']:<20} | {row['tipo']:<4} | {row['natureza']:<8}")
    pause("Clique ENTER para voltar ao submenu.")


def menu_plano_contas(conn: sqlite3.Connection) -> None:
    while True:
        print("\n")
        print("[a] Nova Conta")
        print("[b] Editar Conta")
        print("[c] Excluir Conta")
        print("[d] Detalhar Conta")
        print("[e] Listar todas as contas")
        print("[q] Voltar")
        choice = input("\nEscolha: ").strip().lower()
        if choice == "q":
            return
        if choice not in {"a","b", "c", "d", "e"}:
            pause("Opção inválida. Clique ENTER para tentar novamente.")
            continue
        elif choice == "a":
            nova_conta(conn)
        elif choice == "b":
            editar_conta(conn)
        elif choice == "c":
            # excluir_conta(conn)
            pass
        elif choice == "d":
            detalhar_conta(conn)
        elif choice == "e":
            listar_contas(conn)
