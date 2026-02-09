import streamlit as st
from jinja2 import Template
import pathlib

# Configuração da página
st.set_page_config(page_title="Teste Visual", layout="centered")

st.title("Sistema de Boas-Vindas")

# Campo de entrada no Streamlit
nome_input = st.text_input("Qual o seu nome?")

# Função para renderizar o HTML
def renderizar_layout(nome):
    # Localiza o arquivo na pasta do GitHub
    caminho_base = pathlib.Path(__file__).parent
    caminho_html = caminho_base / "template.html"

    try:
        with open(caminho_html, "r", encoding="utf-8") as f:
            template_html = f.read()
        
        # O Jinja2 faz a troca do {{ nome_usuario }} pelo nome_input
        template_renderizado = Template(template_html).render(nome_usuario=nome)
        
        # Exibe na tela
        st.markdown(template_renderizado, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo: {e}")

# Só mostra o HTML se houver um nome digitado
if nome_input:
    renderizar_layout(nome_input)
else:
    st.info("Digite um nome acima para ver o estilo HTML.")
