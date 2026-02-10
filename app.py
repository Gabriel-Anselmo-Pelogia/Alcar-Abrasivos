import streamlit as st

# ================================
# CONFIGURAÇÃO DA PÁGINA
# ================================
st.set_page_config(
    page_title="Sistema",
    layout="wide"
)

# ================================
# ESTADO GLOBAL
# ================================
if "menu" not in st.session_state:
    st.session_state.menu = "analise"

# ================================
# CAPTURA DO CLIQUE VIA QUERY PARAM
# ================================
params = st.query_params
if "toggle" in params:
    st.session_state.menu = params["toggle"]

# ================================
# FUNÇÃO DO TOGGLE (SEGURA)
# ================================
def toggle_button(label: str, value: str):
    ativo = st.session_state.menu == value

    html = (
        f"<div class='toggle-btn' "
        f"data-active='{str(ativo).lower()}' "
        f"onclick=\"window.location.search='?toggle={value}'\">"
        f"<span>{label}</span>"
        f"</div>"
    )

    st.markdown(html, unsafe_allow_html=True)

# ================================
# SIDEBAR
# ================================
with st.sidebar:
    toggle_button("Análise de Dados", "analise")
    toggle_button("Gerenciamento de Estoque", "estoque")

# ================================
# CONTEÚDO PRINCIPAL
# ================================
st.markdown("## Conteúdo")

if st.session_state.menu == "analise":
    st.success("Você está em **Análise de Dados**")
elif st.session_state.menu == "estoque":
    st.info("Você está em **Gerenciamento de Estoque**")

