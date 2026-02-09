import streamlit as st
from jinja2 import Template
import pathlib

# 1. Configuração da Página
st.set_page_config(page_title="Dashboard Alcar", layout="centered")

# 2. Seus Filtros e Cálculos (O "Funcional")
st.sidebar.header("Filtros do Dashboard")
nome_user = st.sidebar.text_input("Nome do Usuário", "Operador")
valor_venda = st.sidebar.slider("Valor de Venda (R$)", 0, 10000, 4500)
meta = 5000

# Lógica de cálculo para os elementos visuais
progresso = min((valor_venda / meta) * 100, 100) # Limita a 100%
cor_status = "#27ae60" if valor_venda >= meta else "#e67e22"

# 3. Organizando a "Bandeja" de Dados (O Contexto)
contexto = {
    "nome_usuario": nome_user,
    "valor": f"{valor_venda:,.2f}",
    "porcentagem": f"{progresso:.1f}%",
    "cor": cor_status,
    "mensagem": "Meta Batida!" if valor_venda >= meta else "Abaixo da Meta"
}

# 4. Processando o HTML (A união do Bonito com o Funcional)
def renderizar_dashboard(dados):
    caminho_html = pathlib.Path(__file__).parent / "template.html"
    
    if caminho_html.exists():
        with open(caminho_html, "r", encoding="utf-8") as f:
            template_puro = f.read()
        
        # A LINHA QUE FALTAVA:
        # Criamos o objeto Template e renderizamos passando os dados
        template_jinja = Template(template_puro)
        html_final = template_jinja.render(**dados)
        
        # Exibimos com a permissão para HTML
        st.markdown(html_final, unsafe_allow_html=True)
    else:
        st.error("Arquivo template.html não encontrado!")

# 5. Execução
st.title("Monitoramento de Resultados - Alcar")
renderizar_dashboard(contexto)
