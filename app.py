import streamlit as st
from jinja2 import Template
import pathlib

# 1. Configuração inicial
st.set_page_config(page_title="Alcar Dashboard", layout="wide")

# 2. Ler qual página está na URL
# Exemplo: se o link for ?page=estoque, query_params['page'] será 'estoque'
query_params = st.query_params
pagina_atual = query_params.get("page", "analise") # 'analise' é a padrão

# 3. Renderizar o Menu na Sidebar
def render_sidebar_menu():
    path_html = pathlib.Path(__file__).parent / "template.html"
    with open(path_html, "r", encoding="utf-8") as f:
        template = Template(f.read())
    
    # O menu será injetado na sidebar
    st.sidebar.markdown(template.render(), unsafe_allow_html=True)

# Chamada do menu
render_sidebar_menu()

# 4. Lógica de Navegação (Conteúdo Central)
if pagina_atual == "analise":
    st.title("📊 Análise de Dados")
    st.write("Conteúdo da Análise aqui...")

elif pagina_atual == "estoque":
    st.title("📦 Gerenciamento de Estoque")
    st.write("Tabela de estoque aqui...")

elif pagina_atual == "saidas":
    st.title("🚚 Controle de Saídas")

elif pagina_atual == "pendencias":
    st.title("⏳ Pendências")

elif pagina_atual == "pv":
    st.title("📝 Abertura de PV")
