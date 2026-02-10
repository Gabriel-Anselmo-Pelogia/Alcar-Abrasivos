import streamlit as st

st.set_page_config(layout="wide")

# ===============================
# CSS
# ===============================
with open("style.css", "r", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ===============================
# SIDEBAR (MENU)
# ===============================
with st.sidebar:

    # Widget REAL (controle de estado)
    menu = st.radio(
        "",
        ["Análise de Dados", "Gerenciamento de Estoque"],
        label_visibility="collapsed"
    )

    # Visual customizado
    st.markdown(f"""
    <div class="menu-btn {'active' if menu == 'Análise de Dados' else ''}">
        Análise de Dados
    </div>

    <div class="menu-btn {'active' if menu == 'Gerenciamento de Estoque' else ''}">
        Gerenciamento de Estoque
    </div>
    """, unsafe_allow_html=True)

# ===============================
# CONTEÚDO
# ===============================
st.title("Dashboard")

if menu == "Análise de Dados":
    st.success("📊 Página de Análise de Dados")
else:
    st.info("📦 Página de Gerenciamento de Estoque")
