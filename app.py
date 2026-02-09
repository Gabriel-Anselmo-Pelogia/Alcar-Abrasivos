import streamlit as st
import pathlib

# Configuração
st.set_page_config(layout="wide")

# 1. Ler os parâmetros da URL para saber onde estamos
pagina_atual = st.query_params.get("page", "analise")

# 2. Carregar e exibir o menu lateral
def exibir_menu():
    caminho = pathlib.Path(__file__).parent / "template.html"
    with open(caminho, "r", encoding="utf-8") as f:
        html_menu = f.read()
    
    # Renderiza o bloco INTEIRO de uma vez na sidebar
    st.sidebar.markdown(html_menu, unsafe_allow_html=True)

exibir_menu()

# 3. Conteúdo das páginas
if pagina_atual == "analise":
    st.title("📊 Análise de Dados")
elif pagina_atual == "estoque":
    st.title("📦 Gerenciamento de Estoque")
# ... adicione os outros elifs aqui
