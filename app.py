import streamlit as st
from jinja2 import Template
import pathlib

# 1. Configuração da Página
st.set_page_config(page_title="Sistema Alcar", layout="wide")

# 2. MENU NA BARRA LATERAL
with st.sidebar:
    st.header("🏢 Menu Principal")
    
    # Criando os botões de navegação
    menu = st.radio(
        "Selecione uma categoria:",
        [
            "Análise de Dados", 
            "Gerenciamento de Estoque", 
            "Saídas", 
            "Pendências", 
            "Abertura de PV"
        ]
    )
    
    st.divider()
    st.caption("Usuário: Operador Alcar")

# 3. LÓGICA DE NAVEGAÇÃO
# Dependendo do que for clicado no menu, o código abaixo muda
if menu == "Análise de Dados":
    st.title("📊 Análise de Dados")
    # Aqui você chamará seu HTML ou cálculos de análise
    st.info("Carregando indicadores de desempenho...")

elif menu == "Gerenciamento de Estoque":
    st.title("📦 Gerenciamento de Estoque")
    # Aqui você colocará a lógica de estoque
    st.warning("Verificando níveis de produtos...")

elif menu == "Saídas":
    st.title("🚚 Saídas")
    # Lógica de saídas

elif menu == "Pendências":
    st.title("⏳ Pendências")
    # Lógica de pendências

elif menu == "Abertura de PV":
    st.title("📝 Abertura de PV")
    # Lógica de abertura de PV
