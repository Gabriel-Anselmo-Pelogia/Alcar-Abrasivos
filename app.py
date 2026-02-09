import streamlit as st
from jinja2 import Template
import pathlib

# --- CÁLCULOS E FILTROS ---
valor_venda = 7823.00
meta = 10000.00
progresso = (valor_venda / meta) * 100
cor_status = "#27ae60" if progresso >= 100 else "#e67e22"

contexto = {
    "valor": f"{valor_venda:,.2f}",
    "porcentagem": f"{progresso:.1f}%",
    "cor": cor_status,
    "nome_usuario": "Operador Alcar"
}

# --- FUNÇÃO DE CARREGAMENTO SEPARADO ---
def carregar_dashboard():
    # Caminho do arquivo HTML na mesma pasta
    path_html = pathlib.Path(__file__).parent / "template.html"
    
    with open(path_html, "r", encoding="utf-8") as f:
        html_puro = f.read()
    
    # Renderização com Jinja2
    template = Template(html_puro)
    html_final = template.render(**contexto)
    
    # Envio para o Streamlit (O parâmetro essencial)
    st.markdown(html_final, unsafe_allow_html=True)

# Execução
st.title("Painel de Controle")
carregar_dashboard()
