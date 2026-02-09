import streamlit as st

# 1. Configuração da página
st.set_page_config(page_title="Sistema Alcar", layout="wide")

# 2. Carregar o CSS Externo
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("style.css")

# 3. Inicializar o estado da página (Session State)
if 'menu_option' not in st.session_state:
    st.session_state.menu_option = 'Análise de Dados'

# 4. Criar a Barra Lateral
with st.sidebar:
    st.markdown("### 🏢 Menu Principal")
    st.write("---")
    
    # Dicionário de opções: Nome -> Ícone
    menu_items = {
        "Análise de Dados": "📊",
        "Gerenciamento de Estoque": "📦",
        "Saídas": "🚚",
        "Pendências": "⏳",
        "Abertura de PV": "📝"
    }

    # Loop para criar os botões
    for label, icon in menu_items.items():
        is_active = st.session_state.menu_option == label
        # Verificamos se este botão é o que deve estar "Vermelho"
        if st.session_state.menu_option == label:
            # Envolvemos em uma div que o CSS vai identificar como ATIVA
            st.markdown('<div class="btn-ativo">', unsafe_allow_html=True)
            if st.button(
                f"{icon}  {label}",
                key=label,
                type="primary" if is_active else "secondary",
                use_container_width=True
            ):
                pass # Já está na página
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            # Botão normal (Cinza)
            if st.button(f"{icon}  {label}", key=label):
                st.session_state.menu_option = label
                st.rerun()

# 5. Lógica de Conteúdo Central
opcao = st.session_state.menu_option

if opcao == "Análise de Dados":
    st.title("📊 Análise de Dados")
    st.info("Aqui entrarão seus gráficos e indicadores.")
    
elif opcao == "Gerenciamento de Estoque":
    st.title("📦 Gerenciamento de Estoque")
    st.success("Tabela de estoque pronta para edição.")

elif opcao == "Saídas":
    st.title("🚚 Controle de Saídas")

elif opcao == "Pendências":
    st.title("⏳ Lista de Pendências")

elif opcao == "Abertura de PV":
    st.title("📝 Formulário de PV")
