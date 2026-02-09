import streamlit as st
import pathlib
from jinja2 import Template
import streamlit.components.v1 as components

st.set_page_config(page_title="Alcar Abrasivos", layout="wide")

# 1. Gerenciamento do Estado da Página
if 'pagina_ativa' not in st.session_state:
    st.session_state.pagina_ativa = 'analise'

# 2. Captura de cliques do Iframe
# O componente envia o valor para o Python através desta função
def atualizar_navegação():
    query_params = st.query_params
    if "page" in query_params:
        st.session_state.pagina_ativa = query_params["page"]

# 3. Função do Menu
def exibir_menu():
    caminho = pathlib.Path(__file__).parent / "template.html"
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            template_puro = f.read()
        
        template_jinja = Template(template_puro)
        # Passamos a página do Session State para o HTML
        html_final = template_jinja.render(pagina_ativa=st.session_state.pagina_ativa)
        
        with st.sidebar:
            st.markdown("### Navegação")
            # Renderiza o menu
            components.html(html_final, height=500, scrolling=False)
            
            # Script para forçar o Streamlit a ler a URL quando ela mudar dentro do iframe
            # Isso é necessário para sincronizar o clique com o Python
            st.button("🔄 Atualizar Painel", on_click=atualizar_navegação, use_container_width=True)
            
    except Exception as e:
        st.sidebar.error(f"Erro: {e}")

exibir_menu()

# 4. Lógica de Exibição
# Usamos o st.session_state.pagina_ativa para decidir o que mostrar
pag = st.session_state.pagina_ativa

if pag == "analise":
    st.title("📊 Análise de Dados")
    st.info("Painel de indicadores carregado com sucesso.")
elif pag == "estoque":
    st.title("📦 Gerenciamento de Estoque")
elif pag == "saidas":
    st.title("🚚 Saídas")
elif pag == "pendencias":
    st.title("⏳ Pendências")
elif pag == "pv":
    st.title("📝 Abertura de PV")
