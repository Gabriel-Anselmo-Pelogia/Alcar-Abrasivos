import streamlit as st
from pathlib import Path

st.set_page_config(layout="wide")

# Estado
if "menu" not in st.session_state:
    st.session_state.menu = "analise"

# CSS
css = Path("frontend/sidebar.css").read_text()
st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

with st.sidebar:
    if st.button("Análise de Dados", key="analise"):
        st.session_state.menu = "analise"

    if st.button("Gerenciamento de Estoque", key="estoque"):
        st.session_state.menu = "estoque"

# Ativa classe visual
st.markdown("""
<script>
const buttons = parent.document.querySelectorAll(
    '[data-testid="stSidebar"] button'
);
buttons.forEach(btn => {
    if (btn.innerText.includes("Análise") && "%s" === "analise") btn.classList.add("active");
    if (btn.innerText.includes("Gerenciamento") && "%s" === "estoque") btn.classList.add("active");
});
</script>
""" % (st.session_state.menu, st.session_state.menu),
unsafe_allow_html=True)

# Conteúdo
st.title("Conteúdo")

if st.session_state.menu == "analise":
    st.success("📊 Análise de Dados")
else:
    st.info("📦 Gerenciamento de Estoque")
