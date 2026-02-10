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

    col1 = st.container()
    if col1.button("Análise de Dados", key="btn_analise"):
        st.session_state.menu = "analise"

    col2 = st.container()
    if col2.button("Gerenciamento de Estoque", key="btn_estoque"):
        st.session_state.menu = "estoque"

    # HTML visual
    html = Path("frontend/sidebar.html").read_text(encoding="utf-8")

    html = html.replace(
        "{{analise}}",
        "active" if st.session_state.menu == "analise" else ""
    )

    html = html.replace(
        "{{estoque}}",
        "active" if st.session_state.menu == "estoque" else ""
    )

    st.markdown(html, unsafe_allow_html=True)

# Conteúdo
st.title("Conteúdo")

if st.session_state.menu == "analise":
    st.success("📊 Análise de Dados")
else:
    st.info("📦 Gerenciamento de Estoque")
