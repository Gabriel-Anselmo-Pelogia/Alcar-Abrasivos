import streamlit as st
from pathlib import Path

st.set_page_config(layout="wide")

# Estado
if "menu" not in st.session_state:
    st.session_state.menu = "analise"

# CSS
css = Path("frontend/sidebar.css").read_text(encoding="utf-8")
st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

with st.sidebar:
    if st.button("Análise de Dados"):
        st.session_state.menu = "analise"

    if st.button("Gerenciamento de Estoque"):
        st.session_state.menu = "estoque"

# HTML base
html = Path("frontend/sidebar.html").read_text(encoding="utf-8")

# Injeta classe ativa (SEM format, SEM f-string)
html = html.replace(
    "{{analise}}",
    "active" if st.session_state.menu == "analise" else ""
)

html = html.replace(
    "{{estoque}}",
    "active" if st.session_state.menu == "estoque" else ""
)

# Renderiza HTML estilizado
st.sidebar.markdown(html, unsafe_allow_html=True)

# Conteúdo
st.title("Conteúdo")

if st.session_state.menu == "analise":
    st.success("📊 Análise de Dados")
else:
    st.info("📦 Gerenciamento de Estoque")

