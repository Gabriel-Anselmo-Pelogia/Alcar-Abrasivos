import streamlit as st

# ================================
# CONFIGURAÇÃO DA PÁGINA
# ================================
st.set_page_config(
    page_title="Sistema",
    layout="wide"
)

# ================================
# CSS – INJETADO NO APP
# ================================
st.markdown("""
<style>
/* SIDEBAR – TOGGLE ESTILO PILL */

[data-testid="stSidebar"] .toggle-btn {
    position: relative;
    width: 100%;
    height: 56px;
    margin-bottom: 12px;
    padding-left: 64px;

    display: flex;
    align-items: center;

    border-radius: 30px;
    font-size: 14px;
    font-weight: 600;
    color: white;

    background: #bfbfbf;
    cursor: pointer;
    user-select: none;

    transition: background 0.35s ease, filter 0.2s ease;
}

[data-testid="stSidebar"] .toggle-btn[data-active="true"] {
    background: linear-gradient(90deg, #ef4444, #b91c1c);
    box-shadow: 0 10px 25px rgba(185, 28, 28, 0.45);
}

[data-testid="stSidebar"] .toggle-btn span {
    pointer-events: none;
}

[data-testid="stSidebar"] .toggle-btn::before {
    content: "";
    position: absolute;
    top: 50%;
    left: 8px;

    width: 40px;
    height: 40px;
    border-radius: 50%;

    background: white;
    box-shadow: 0 4px 10px rgba(0,0,0,0.25);

    transform: translateY(-50%);
    transition:
        left 0.55s cubic-bezier(0.22, 1, 0.36, 1),
        box-shadow 0.3s ease;
}

[data-testid="stSidebar"] .toggle-btn[data-active="true"]::before {
    left: calc(100% - 48px);
    box-shadow:
        0 0 0 4px rgba(255,255,255,0.25),
        0 6px 14px rgba(0,0,0,0.35);
}

[data-testid="stSidebar"] .toggle-btn:hover {
    filter: brightness(1.08);
}
</style>
""", unsafe_allow_html=True)

# ================================
# ESTADO GLOBAL
# ================================
if "menu" not in st.session_state:
    st.session_state.menu = "analise"

# ================================
# CAPTURA DO CLIQUE (QUERY PARAM)
# ================================
params = st.query_params
if "toggle" in params:
    st.session_state.menu = params["toggle"]

# ================================
# FUNÇÃO DO TOGGLE
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
# SIDEBAR (AQUI É O PONTO-CHAVE)
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
