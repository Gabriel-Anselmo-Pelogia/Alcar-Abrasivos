import streamlit as st
from pathlib import Path

st.set_page_config(layout="wide")

# Estado
if "menu" not in st.session_state:
    st.session_state.menu = "analise"

# Captura clique
params = st.query_params
if "toggle" in params:
    st.session_state.menu = params["toggle"]

# Lê HTML
html = Path("frontend/sidebar.html").read_text(encoding="utf-8")

# Injeta atributo data-active
html = html.replace(
    "{{analise}}",
    'data-active="true"' if st.session_state.menu == "analise" else ""
)

html = html.replace(
    "{{estoque}}",
    'data-active="true"' if st.session_state.menu == "estoque" else ""
)

# Sidebar
with st.sidebar:
    st.markdown(html, unsafe_allow_html=True)

# Conteúdo
st.title("Conteúdo")

if st.session_state.menu == "analise":
    st.success("📊 Análise de Dados")
else:
    st.info("📦 Gerenciamento de Estoque")
