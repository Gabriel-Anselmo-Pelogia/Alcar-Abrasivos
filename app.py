import streamlit as st
import pathlib
from jinja2 import Template
import streamlit.components.v1 as components

# 1. Configuração da Página (DEVE ser a primeira linha de comando Streamlit)
st.set_page_config(page_title="Alcar Abrasivos", layout="wide")

# 2. DEFINIÇÃO DA VARIÁVEL (Onde o erro acontecia)
# Lemos os parâmetros da URL. Se estiver vazio, o padrão é 'analise'
pagina_atual = st.query_params.get("page", "analise")

# 3. Função para Renderizar o Menu
def exibir_menu():
    caminho = pathlib.Path(__file__).parent / "template.html"
    
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            template_puro = f.read()
        
        # Renderiza o Jinja2 passando a variável para o HTML
        template_jinja = Template(template_puro)
        html_final = template_jinja.render(pagina_ativa=pagina_atual)
        
        # Injeta na Sidebar usando o componente de HTML isolado (iframe)
        # Isso evita que o código apareça como texto puro
        with st.sidebar:
            st.markdown("### Navegação")
            components.html(html_final, height=500, scrolling=False)
            
    except Exception as e:
        st.sidebar.error(f"Erro ao carregar menu: {e}")

# 4. EXECUÇÃO DO MENU
exibir_menu()

# 5. LÓGICA DE NAVEGAÇÃO (Agora a variável 'pagina_atual' existe com certeza)
if pagina_atual == "analise":
    st.title("📊 Análise de Dados")
    st.write("Conteúdo da Análise...")

elif pagina_atual == "estoque":
    st.title("📦 Gerenciamento de Estoque")
    st.write("Conteúdo do Estoque...")

elif pagina_atual == "saidas":
    st.title("🚚 Saídas")
    st.write("Conteúdo de Saídas...")

elif pagina_atual == "pendencias":
    st.title("⏳ Pendências")
    st.write("Conteúdo de Pendências...")

elif pagina_atual == "pv":
    st.title("📝 Abertura de PV")
    st.write("Conteúdo de PV...")
