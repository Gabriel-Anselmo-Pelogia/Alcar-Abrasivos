import streamlit as st
from jinja2 import Template
import pathlib

# 1. Configuração da Página
st.set_page_config(page_title="Dashboard Alcar", layout="wide")

# 2. BARRA LATERAL (Isso fará ela reaparecer)
st.sidebar.header("Filtros de Controle")

# Criando os inputs que o usuário pode mexer
nome_sidebar = st.sidebar.text_input("Usuário", value="Operador Alcar")
valor_venda = st.sidebar.number_input("Valor Atual (R$)", min_value=0.0, value=7823.0)
meta_objetivo = st.sidebar.number_input("Meta (R$)", min_value=1.0, value=10000.0)

# 3. Lógica de Cálculo (Funcional)
progresso = (valor_venda / meta_objetivo) * 100
# Limita o preenchimento da barra a 100% no visual para não quebrar o layout
porcentagem_visual = min(progresso, 100)
cor_status = "#27ae60" if progresso >= 100 else "#e67e22"

# 4. Organização do Contexto para o HTML
contexto = {
    "valor": f"{valor_venda:,.2f}",
    "porcentagem": f"{porcentagem_visual:.1f}%",
    "cor": cor_status,
    "nome_usuario": nome_sidebar
}

# 5. Função para carregar o HTML Externo
def renderizar_layout():
    path_html = pathlib.Path(__file__).parent / "template.html"
    
    try:
        with open(path_html, "r", encoding="utf-8") as f:
            template_puro = f.read()
        
        # Renderiza os dados no template
        html_final = Template(template_puro).render(**contexto)
        
        # Exibe no Streamlit
        st.markdown(html_final, unsafe_allow_html=True)
    except FileNotFoundError:
        st.error("Arquivo 'template.html' não encontrado no repositório.")

# Execução na tela principal
st.title("Painel de Monitoramento")
renderizar_layout()

# Você pode até adicionar um gráfico do Streamlit aqui embaixo se quiser
st.divider()
st.caption("Dados atualizados em tempo real via automação.")
