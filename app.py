import streamlit as st
import pathlib
from jinja2 import Template

def exibir_menu():
    caminho = pathlib.Path(__file__).parent / "template.html"
    
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            template_puro = f.read()
        
        # Renderiza o Jinja2
        template_jinja = Template(template_puro)
        html_final = template_jinja.render(pagina_ativa=pagina_atual)
        
        # LIMPEZA CRUCIAL: Remove quebras de linha para o Streamlit não achar que é Markdown
        html_limpo = html_final.replace("\n", "").replace("\r", "")
        
        # Injeção na Sidebar com identificador HTML claro
        st.sidebar.markdown(f"<div>{html_limpo}</div>", unsafe_allow_html=True)
        
    except Exception as e:
        st.sidebar.error(f"Erro ao carregar menu: {e}")

# ... resto do código (configuração de página e lógica de navegação)

# --- EXECUÇÃO DO MENU ---
exibir_menu()

# 4. Lógica de Navegação (Conteúdo Central)
# Aqui você colocará o código funcional de cada parte futuramente.
if pagina_atual == "analise":
    st.title("📊 Análise de Dados")
    st.write("Bem-vindo à área de análise. Seus gráficos aparecerão aqui.")

elif pagina_atual == "estoque":
    st.title("📦 Gerenciamento de Estoque")
    st.write("Controle de entrada e saída de materiais.")

elif pagina_atual == "saidas":
    st.title("🚚 Saídas")
    st.write("Monitoramento de expedição.")

elif pagina_atual == "pendencias":
    st.title("⏳ Pendências")
    st.write("Lista de tarefas e pedidos aguardando ação.")

elif pagina_atual == "pv":
    st.title("📝 Abertura de PV")
    st.write("Formulário para abertura de Pedidos de Venda.")
