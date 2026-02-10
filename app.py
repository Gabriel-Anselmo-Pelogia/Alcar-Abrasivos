import streamlit as st

st.set_page_config(layout="wide")

# -------------------------------
# CSS
# -------------------------------
with open("style.css", "r", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# -------------------------------
# SIDEBAR
# -------------------------------
with st.sidebar:

    # Widget real (estado)
    menu = st.radio(
        "",
        ["Análise de Dados", "Gerenciamento de Estoque"],
        label_visibility="collapsed"
    )

    # Menu visual
    active_analise = "active" if menu == "Análise de Dados" else ""
    active_estoque = "active" if menu == "Gerenciamento de Estoque" else ""

    st.markdown(f"""
    <div class="menu-btn {active_analise}">
        Análise de Dados
    </div>

    <div class="menu-btn {active_estoque}">
        Gerenciamento de Estoque
    </div>
    """, unsafe_allow_html=True)

# -------------------------------
# CONTEÚDO PRINCIPAL
# -------------------------------
st.title("Dashboard")

if menu == "Análise de Dados":
    st.success("📊 Página de Análise de Dados")
else:
    st.info("📦 Página de Gerenciamento de Estoque")
