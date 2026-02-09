import streamlit as st
import pathlib

# 1. Configuração inicial
st.set_page_config(page_title="Alcar Abrasivos", layout="wide")

# 2. Função para carregar o CSS externo
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css("style.css")

# 3. Estado da Navegação (Session State)
if 'pagina' not in st.session_state:
    st.session_state.pagina = 'Análise de Dados'

# 4. Menu Lateral
with st.sidebar:
    st.title("🏢 Menu Principal")
    
    opcoes = {
        "Análise de Dados": "📊",
        "Gerenciamento de Estoque": "📦",
        "Saídas": "🚚",
        "Pendências": "⏳",
        "Abertura de PV": "📝"
    }

    for nome, icone in opcoes.items():
        # Se for a página ativa, aplica a classe CSS 'btn-ativo'
        if st.session_state.pagina == nome:
            st.markdown('<div class="btn-ativo">', unsafe_allow_html=True)
            st.button(f"{icone} {nome}", key=nome) # Botão já está ativo
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            # Botão normal (Cinza)
            if st.button(f"{icone} {nome}", key=nome):
                st.session_state.pagina = nome
                st.rerun()

# 5. Área de Conteúdo
pag = st.session_state.pagina

st.divider() # Linha visual

if pag == "Análise de Dados":
    st.header("📊 Análise de Dados")
    # Seu código de análise entra aqui
elif pag == "Gerenciamento de Estoque":
    st.header("📦 Gerenciamento de Estoque")
# ... adicione os demais elifs aqui
