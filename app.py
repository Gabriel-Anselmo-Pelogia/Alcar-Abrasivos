import streamlit as st
import pathlib
from jinja2 import Template

# 1. Configuração da Página
st.set_page_config(page_title="Alcar Abrasivos", layout="wide")

# 2. Captura da Página Atual via URL (Query Params)
# Se não houver nada na URL, o padrão é 'analise'
pagina_atual = st.query_params.get("page", "analise")

# 3. Função para Renderizar o Menu Lateral
def exibir_menu():
    # Localiza o arquivo template.html na mesma pasta do app.py
    caminho = pathlib.Path(__file__).parent / "template.html"
    
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            template_puro = f.read()
        
        # O Jinja2 processa o HTML e decide qual botão recebe a classe 'active'
        template_jinja = Template(template_puro)
        html_final = template_jinja.render(pagina_ativa=pagina_atual)
        
        # Injetamos o HTML na Sidebar. 
        # Usamos markdown com unsafe_allow_html para garantir que o CSS seja lido.
        st.sidebar.markdown(html_final, unsafe_allow_html=True)
        
    except FileNotFoundError:
        st.sidebar.error("Erro: Arquivo 'template.html' não encontrado.")

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
