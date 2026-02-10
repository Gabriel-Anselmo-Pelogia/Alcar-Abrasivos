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

    # ITEM 1
    container1 = st.container()
    with container1:
        if st.button("Análise de Dados", key="btn_analise"):
            st.session_state.menu = "analise"

        html = Path("frontend/sidebar.html").read_text(encoding="utf-8")
        html = html.replace(
            "{{analise}}",
            "active" if st.session_state.menu == "analise" else ""
        )
        html = html.replace("{{estoque}}", "")
        st.markdown(html.split("</div>", 1)[0] + "</div>", unsafe_allow_html=True)

    # ITEM 2
    container2 = st.container()
    with container2:
        if st.button("Gerenciamento de Estoque", key="btn_estoque"):
            st.session_state.menu = "estoque"

        html = Path("frontend/sidebar.html").read_text(encoding="utf-8")
        html = html.replace(
            "{{estoque}}",
            "active" if st.session_state.menu == "estoque" else ""
        )
        html = html.replace("{{analise}}", "")
        st.markdown(html.split("</div>", 1)[1], unsafe_allow_html=True)

# Conteúdo
st.title("Conteúdo")

if st.session_state.menu == "analise":
    st.success("📊 Análise de Dados")
else:
    st.info("📦 Gerenciamento de Estoque")

