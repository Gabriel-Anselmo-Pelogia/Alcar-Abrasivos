import streamlit as st
import pathlib

st.set_page_config(page_title="Alcar Abrasivos", layout="wide")

# Função para carregar o CSS
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css("style.css")

# Estado da página
if 'pagina' not in st.session_state:
    st.session_state.pagina = 'Análise de Dados'

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
        # Verificamos se esta opção é a ativa
        is_active = st.session_state.pagina == nome
        
        # Criamos um container. Se for ativo, adicionamos a classe 'btn-ativo'
        # Usamos uma f-string para aplicar a classe condicionalmente
        classe_css = "btn-ativo" if is_active else "btn-container"
        
        with st.container():
            st.markdown(f'<div class="{classe_css}">', unsafe_allow_html=True)
            if st.button(f"{icone} {nome}", key=f"btn_{nome}"):
                st.session_state.pagina = nome
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

# Conteúdo Central
st.header(f"{st.session_state.pagina}")

# 5. Área de Conteúdo
pag = st.session_state.pagina

st.divider() # Linha visual

if pag == "Análise de Dados":
    st.header("📊 Análise de Dados")
    # Seu código de análise entra aqui
elif pag == "Gerenciamento de Estoque":
    st.header("📦 Gerenciamento de Estoque")
# ... adicione os demais elifs aqui
