from pathlib import Path
import streamlit as st

css_file = Path(__file__).parent / "style.css"
with open(css_file, "r", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.set_page_config(
    page_title="Sistema Administrativo",
    layout="wide"
)

# Título do sistema
st.markdown("## Sistema Administrativo")

# Painel superior com 5 abas
aba1, aba2, aba3, aba4, aba5 = st.tabs([
    "Aba 01",
    "Aba 02",
    "Aba 03",
    "Aba 04",
    "Aba 05"
])

# -------------------------
# ABA 01
# -------------------------
with aba1:
    st.subheader("Aba 01")
    st.write("Conteúdo da Aba 01")

# -------------------------
# ABA 02
# -------------------------
with aba2:
    st.subheader("Aba 02")
    st.write("Conteúdo da Aba 02")

# -------------------------
# ABA 03
# -------------------------
with aba3:
    st.subheader("Aba 03")
    st.write("Conteúdo da Aba 03")

# -------------------------
# ABA 04
# -------------------------
with aba4:
    st.subheader("Aba 04")
    st.write("Conteúdo da Aba 04")

# -------------------------
# ABA 05
# -------------------------
with aba5:
    st.subheader("Aba 05")
    st.write("Conteúdo da Aba 05")
