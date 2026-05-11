import requests
from bs4 import BeautifulSoup
import pandas as pd


def buscar_campo(soup, nome_campo):

    # percorre todas as células da tabela
    campos = soup.select("td")

    for td in campos:

        texto = td.get_text(strip=True)

        # procura o nome do campo
        if nome_campo in texto:

            # pega a próxima coluna (td irmã)
            proximo_td = td.find_next_sibling("td")

            if proximo_td:
                return proximo_td.get_text(strip=True)

    return None

def print_campo(campos, valores):

    for campo, valor in zip(campos, valores):
        print(f"{campo}: {valor}")

def converter_para_numero(texto):
    
    if texto is None:
        return None

    # Remove pontos e vírgulas
    texto = texto.replace(".", "").replace(",", ".")

    try:
        return float(texto)
    except ValueError:
        return None

def buscar_campos_dataframe(soup, nomes_campos):

    dados = {nome_campo: buscar_campo(soup, nome_campo) for nome_campo in nomes_campos}

    print_campo(nomes_campos, dados.values())

    # Mantém os campos na ordem recebida no argumento.
    return pd.DataFrame([dados], columns=nomes_campos)


# ==========================================
# URL
# ==========================================

url = "https://www.fundamentus.com.br/detalhes.php?papel=ABEV3"

headers = {
    "User-Agent": (
        "Mozilla/5.0 "
        "(X11; Linux x86_64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/120 Safari/537.36"
    )
}

# ==========================================
# REQUEST
# ==========================================

response = requests.get(url, headers=headers)

# ==========================================
# BEAUTIFULSOUP
# ==========================================

soup = BeautifulSoup(response.text, "lxml")

# ==========================================
# EXTRAÇÃO DOS DADOS
# ==========================================

# papel = buscar_campo(soup, "Papel")

# cotacao = buscar_campo(soup, "Cotação")

# numero_acoes = buscar_campo(soup, "Nro. Ações")

# ativo = buscar_campo(soup, "Ativo")

# disponibilidades = buscar_campo(soup, "Disponibilidades")

# ativo_circulante = buscar_campo(soup, "Ativo Circulante")

campos = [
    "Papel",
    "Cotação",
    "Nro. Ações",
    "Ativo",
    "Disponibilidades",
    "Ativo Circulante",
    "Dív. Bruta",
    "Dív. Líquida",
    "Patrim. Líq",
]

df_campos = buscar_campos_dataframe(soup, campos)

# ==========================================
# PRINT NORMAL
# ==========================================

# print("PAPEL:", papel)

# print("COTAÇÃO:", cotacao)

# print("NÚMERO DE AÇÕES:", numero_acoes)

# print("ATIVO:", ativo)

# print("DISPONIBILIDADES:", disponibilidades)

# print("ATIVO CIRCULANTE:", ativo_circulante)

print("\nDATAFRAME:")
print(df_campos)