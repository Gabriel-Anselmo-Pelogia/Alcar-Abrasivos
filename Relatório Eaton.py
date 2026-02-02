import streamlit as st
import pandas as pd
import os
import numpy as np
from datetime import datetime, timedelta

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Sistema Alcar", layout="wide")

# 2. CSS AVANÇADO - IDENTIDADE VISUAL
st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #262730 !important; }
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] div.element-container,
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] div.stButton,
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] div.stButton > button {
        width: 100% !important;
    }
    [data-testid="stSidebar"] div.stButton > button {
        background-color: #3e404b !important;
        color: white !important;
        border: 1px solid #4f515d !important;
        padding: 14px 10px !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        text-align: center !important;
        margin-bottom: 5px !important;
    }
    [data-testid="stSidebar"] div.stButton > button:hover {
        background-color: #ea2a33 !important;
        border-color: #ea2a33 !important;
    }
    h1, h2, h3, .stSubheader { color: #ea2a33 !important; }
    hr { border-top: 2px solid #ea2a33; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÕES AUXILIARES ---
def fmt_br(valor, casas=2):
    try:
        return f"{valor:,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except:
        return valor

def cor_status(status):
    cores = {
        "Excedente": "background-color: #4b0082; color: white;",
        "Alto": "background-color: #1e90ff; color: white;",
        "Ok": "background-color: #2e8b57; color: white;",
        "Confirmar": "background-color: #ffd700; color: black;",
        "Crítico": "background-color: #ea2a33; color: white;",
        "Sem uso": "background-color: #808080; color: white;"
    }
    return cores.get(status, "")

def filtrar_local(df, ano_sel, meses_sel):
    df['Ano'] = pd.to_numeric(df['Ano'], errors='coerce')
    df['Mês'] = pd.to_numeric(df['Mês'], errors='coerce')
    temp_df = df[df['Ano'] == ano_sel]
    if "Média Anual" not in meses_sel and meses_sel:
        meses_lista = [int(m) for m in meses_sel]
        temp_df = temp_df[temp_df['Mês'].isin(meses_lista)]
    return temp_df

def calc_teto(df, colunas):
    if df.empty: return 10
    max_val = df[colunas].max()
    return max_val * MARGEM_GRAFICO if max_val > 0 else 10

def filtrar_periodo(df, ano, meses):
    if "Média Anual" in meses: return df[df['Ano'] == ano]
    return df[(df['Ano'] == ano) & (df['Mês'].isin(meses))]


# --- CONFIGURAÇÕES GERAIS ---
caminho = "Base de dados (Dashboard).xlsx"
COR_EATON = "#ea2a33"
MARGEM_GRAFICO = 1.25
FATOR_IMPOSTO = 0.7275
LINHAS_OFICIAIS = ["LINHA 01", "LINHA 02/HV", "LINHA 03", "LINHA 04", "LINHA 05", "LINHA 06", "LINHA 07", "LINHA 08",
                   "LINHA 09", "LINHA 10/BV MOD 2", "LINHA 11", "LINHA 13", "LINHA 14", "AFTM"]
OPERACOES_PERMITIDAS = ["15A", "15G", "15PC/OM2", "15S", "21A", "ARRASTE", "BORAZON", "EMB", "HSF", "HSG", "LIXADEIRA",
                        "OP25"]


@st.cache_data
def carregar_dados():
    try:
        df_s_raw = pd.read_excel(caminho, sheet_name='Saidas', usecols="B:K")
        df_p_raw = pd.read_excel(caminho, sheet_name='Produção', usecols="B:F", skiprows=1)
        df_est_raw = pd.read_excel(caminho, sheet_name='Estoque', usecols="B:F", skiprows=1)
        df_pv = pd.read_excel(caminho, sheet_name='PEDIDOS', usecols="B:L", skiprows=1)

        df_pv.columns = df_pv.columns.str.strip().str.upper()
        df_pv['DATA'] = pd.to_datetime(df_pv['DATA'], errors='coerce')

        df_est_raw.columns = ['Código Eaton', 'CodAlcar', 'Descrição', 'Valor Unit.', 'Saldo']
        df_est = df_est_raw.groupby('Código Eaton').agg(
            {'Descrição': 'first', 'Valor Unit.': 'mean', 'Saldo': 'sum'}).reset_index()
        df_est['Valor Total'] = df_est['Saldo'] * df_est['Valor Unit.']

        for df in [df_s_raw, df_p_raw]:
            df['Linha'] = df['Linha'].astype(str).str.strip().str.upper()
            df['Data'] = pd.to_datetime(df['Data'])
            df['Ano'] = df['Data'].dt.year
            df['Mês'] = df['Data'].dt.month

        df_s_raw['Valor Total'] = (df_s_raw['Qtd'] * df_s_raw['Valor Unit.']) * FATOR_IMPOSTO
        df_s = df_s_raw[df_s_raw['Linha'].isin(LINHAS_OFICIAIS)].copy()
        df_p = df_p_raw[df_p_raw['Linha'].isin(LINHAS_OFICIAIS)].copy()

        hoje = datetime.now()
        df_s_60d = df_s_raw[df_s_raw['Data'] >= (hoje - timedelta(days=60))].copy()
        uso_60d = df_s_60d.groupby('Código')['Qtd'].sum().reset_index().rename(columns={'Código': 'Código Eaton', 'Qtd': 'Uso 60d'})
        df_est = pd.merge(df_est, uso_60d, on='Código Eaton', how='left').fillna(0)

        def calc_status(row):
            uso, saldo = row['Uso 60d'], row['Saldo']
            if uso <= 0: return 0, "Sem uso"
            dias = round(saldo / (uso / 60))
            if dias >= 120: st_val = "Excedente"
            elif dias >= 75: st_val = "Alto"
            elif dias >= 30: st_val = "Ok"
            elif dias >= 15: st_val = "Confirmar"
            else: st_val = "Crítico"
            return dias, st_val

        df_est[['Dias Cobertura', 'Situação']] = df_est.apply(lambda r: pd.Series(calc_status(r)), axis=1)
        return df_s, df_p, df_s_raw, df_p_raw, df_est, df_s_60d, df_pv
    except Exception as e:
        st.error(f"Erro ao carregar Excel: {e}")
        return None, None, None, None, None, None, None


# CARREGAMENTO INICIAL
df_s, df_p, df_s_raw, df_p_raw, df_est, df_s_60d, df_pv = carregar_dados()
meses_n = {1: 'Jan', 2: 'Fev', 3: 'Mar', 4: 'Abr', 5: 'Mai', 6: 'Jun', 7: 'Jul', 8: 'Ago', 9: 'Set', 10: 'Out',
           11: 'Nov', 12: 'Dez'}
try:
    # Lendo a aba PCP para criar o dicionário de prazos
    df_prazos_pcp = pd.read_excel(caminho, sheet_name="PCP", skiprows=1)
    df_prazos_pcp.columns = [str(c).strip().upper() for c in df_prazos_pcp.columns]

    # Criando o mapa: Coluna 1 (B) é o código, Coluna 2 (C) é o prazo
    mapa_prazos = dict(zip(df_prazos_pcp.iloc[:, 1].astype(str).str.strip(), df_prazos_pcp.iloc[:, 2]))
except Exception as e:
    # Se a aba não existir ou der erro, cria um mapa vazio para não travar o código
    mapa_prazos = {}
    st.sidebar.warning("Aba 'PCP' não encontrada ou fora do padrão.")

if df_s is not None:
    if 'pagina' not in st.session_state: st.session_state.pagina = "Análise"

    with st.sidebar:
        # Espaçamento e Centralização da Logo
        caminho_logo = r"C:\Users\filial.eaton\Desktop\Novo Dashboard\Planilhas\Logo Alcar.png"
        if os.path.exists(caminho_logo):
            col_l1, col_l2, col_l3 = st.columns([0.5, 5, 0.5])
            with col_l2:
                st.image(caminho_logo, use_container_width=True)
        else:
            st.markdown("<h2 style='text-align: center; color: white;'>ALCAR ABRASIVOS</h2>", unsafe_allow_html=True)

            st.markdown("---")
        if st.button("📊 ANÁLISE DE DADOS"): st.session_state.pagina = "Análise"
        if st.button("📦 ESTOQUE"): st.session_state.pagina = "Estoque"
        if st.button("📑 SAÍDAS"): st.session_state.pagina = "Saídas"
        if st.button("📝 ABERTURA DE PV"): st.session_state.pagina = "Abertura de PV"
        if st.button("🚀 SUGESTÃO DE COMPRAS"): st.session_state.pagina = "Compras"

    # --- PÁGINA 1: ANÁLISE ---
    if st.session_state.pagina == "Análise":
        st.title("📊 Painel Industrial")

        # 1. SEÇÃO DE FILTROS DO TOPO (Dividida em Colunas)
        st.header("1. Comparativo Custo Peça")
        c1, c2 = st.columns([1, 4])

        with c1:
            a1 = st.selectbox("Ano A", sorted(df_s['Ano'].unique()), key='a1')
            a2 = st.selectbox("Ano B", sorted(df_s['Ano'].unique()), key='a2')
            op_mes = ["Média Anual"] + list(range(1, 13))
            p1 = st.multiselect("Mês A", op_mes, format_func=lambda x: meses_n.get(x, x), default="Média Anual",
                                key='p1')
            p2 = st.multiselect("Mês B", op_mes, format_func=lambda x: meses_n.get(x, x), default="Média Anual",
                                key='p2')

        with c2:
            def preparar_g1(ano, meses):
                fs, fp = filtrar_periodo(df_s, ano, meses), filtrar_periodo(df_p, ano, meses)
                res = pd.concat([fs.groupby('Linha')['Valor Total'].sum(), fp.groupby('Linha')['Quantidade'].sum()],
                                    axis=1).fillna(0)
                res['CP'] = (res['Valor Total'] / res['Quantidade']).replace([float('inf')], 0).fillna(0)
                res = res.reindex(LINHAS_OFICIAIS).fillna(0).reset_index()

                gs, gp = filtrar_periodo(df_s_raw, ano, meses), filtrar_periodo(df_p_raw, ano, meses)
                med_p = gs['Valor Total'].sum() / gp['Quantidade'].sum() if gp['Quantidade'].sum() > 0 else 0
                bench = pd.DataFrame({'Linha': ['MÉDIA PLANTA'], 'CP': [med_p]})
                return pd.concat([res, bench], ignore_index=True)


            d1, d2 = preparar_g1(a1, p1), preparar_g1(a2, p2)
            fig1 = go.Figure([
                go.Bar(name='Período A', x=d1['Linha'], y=d1['CP'], marker_color=COR_EATON,
                        text=d1['CP'].apply(lambda x: f'R$ {fmt_br(x, 3)}'), textposition='outside'),
                go.Bar(name='Período B', x=d2['Linha'], y=d2['CP'], marker_color='#555555',
                        text=d2['CP'].apply(lambda x: f'R$ {fmt_br(x, 3)}'), textposition='outside')
            ])
            st.write("### Gráfico Comparativo")
            st.plotly_chart(fig1.update_layout(barmode='group', height=400,
                                                yaxis=dict(range=[0, max(d1['CP'].max(), d2['CP'].max()) * 1.3])),
                            use_container_width=True)

        # =====================================================================
        # FINAL DAS COLUNAS SUPERIORES - DAQUI PARA BAIXO TELA CHEIA
        # =====================================================================

        # --- SEÇÃO 2: RANKING GERAL DE CONSUMO ---
        st.markdown("---")
        st.subheader("📊 Ranking Geral por Operação")

        # 1. Filtros de Período
        cr0, cr1, cr2, cr3, cr4 = st.columns([1, 1, 1.5, 1, 1.5])

        with cr0:
            tipo_rk = st.radio("Métrica:", ["R$", "Qtd"], horizontal=True, key='rk_geral_tipo')
        with cr1:
            rk_a1 = st.selectbox("Ano A", sorted(df_s['Ano'].unique()), key='rk_geral_a1')
        with cr2:
            rk_p1 = st.multiselect("Mês A", ["Média Anual"] + list(range(1, 13)),
                                   format_func=lambda x: meses_n.get(x, x), default="Média Anual",
                                   key='rk_geral_p1')
        with cr3:
            rk_a2 = st.selectbox("Ano B", sorted(df_s['Ano'].unique()), key='rk_geral_a2')
        with cr4:
            rk_p2 = st.multiselect("Mês B", ["Média Anual"] + list(range(1, 13)),
                                   format_func=lambda x: meses_n.get(x, x), default="Média Anual",
                                   key='rk_geral_p2')

        col_metrica = 'Valor Total' if tipo_rk == "R$" else 'Qtd'

        # 2. SEM FILTRO DE OPERAÇÃO: Usamos a base completa
        # Apenas garantimos que a coluna 'Operação' seja tratada como texto para não dar erro no gráfico
        df_rk_base = df_s.copy()
        df_rk_base['Operação'] = df_rk_base['Operação'].astype(str).str.strip()

        # 3. Processamento usando a função filtrar_local (que deve estar no topo do script)
        data_a = filtrar_local(df_rk_base, rk_a1, rk_p1)
        data_b = filtrar_local(df_rk_base, rk_a2, rk_p2)

        # Agrupamento Período A
        res_a = data_a.groupby('Operação')[col_metrica].sum().reset_index() if not data_a.empty else pd.DataFrame(
            columns=['Operação', col_metrica])
        res_a['Período'] = 'Período A'

        # Agrupamento Período B
        res_b = data_b.groupby('Operação')[col_metrica].sum().reset_index() if not data_b.empty else pd.DataFrame(
            columns=['Operação', col_metrica])
        res_b['Período'] = 'Período B'

        # 4. União e Ordenação (Top 10 Geral para não poluir o gráfico)
        df_final_rk = pd.concat([res_a, res_b])

        if not res_a.empty or not res_b.empty:
            # Define a ordem baseada no maior consumo do Período A
            # .head(10) garante que o gráfico mostre apenas as 10 maiores operações totais
            ordem_final = res_a.sort_values(col_metrica, ascending=False).head(10)['Operação'].tolist()

            # Filtramos o dataframe final para mostrar apenas esses Top 10
            df_plot = df_final_rk[df_final_rk['Operação'].isin(ordem_final)]

            fig_rk = px.bar(
                df_plot,
                x='Operação',
                y=col_metrica,
                color='Período',
                barmode='group',
                text=col_metrica,
                category_orders={"Operação": ordem_final},
                color_discrete_map={'Período A': COR_EATON, 'Período B': '#555555'}
            )

            fmt = 'R$ %{text:.2s}' if col_metrica == 'Valor Total' else '%{text:.0f}'
            fig_rk.update_traces(textposition='outside', texttemplate=fmt)
            fig_rk.update_layout(yaxis=dict(range=[0, calc_teto(df_plot, col_metrica) * 1.3]))

            st.plotly_chart(fig_rk, use_container_width=True)
        else:
            st.info("Nenhum dado encontrado para o período selecionado.")

        # --- SEÇÃO 3: EVOLUÇÃO (Também em tela cheia) ---
        st.markdown("---")
        # ... (Restante do seu código de evolução)
        st.header("3. Evolução de Performance")
        cl, ca = st.columns(2)
        with cl:
            sel_l = st.selectbox("Escolha a Linha", LINHAS_OFICIAIS)
        with ca:
            sel_a_ev = st.selectbox("Escolha o Ano", sorted(df_s['Ano'].unique()), key='ev_ano')
        ds_l = df_s[(df_s['Linha'] == sel_l) & (df_s['Ano'] == sel_a_ev)].groupby('Mês')[
            'Valor Total'].sum().reset_index()
        dp_l = df_p[(df_p['Linha'] == sel_l) & (df_p['Ano'] == sel_a_ev)].groupby('Mês')[
            'Quantidade'].sum().reset_index()
        df_ev = pd.merge(pd.DataFrame({'Mês': range(1, 13)}), ds_l, on='Mês', how='left').merge(dp_l, on='Mês',
                                                                                                how='left').fillna(0)
        df_ev['CP'] = (df_ev['Valor Total'] / df_ev['Quantidade']).fillna(0)
        c_ev1, c_ev2, c_ev3 = st.columns(3)
        with c_ev1:
            st.plotly_chart(go.Figure(go.Bar(x=df_ev['Mês'].apply(lambda x: meses_n[x]), y=df_ev['CP'],
                                             marker_color=COR_EATON)).update_layout(title="Custo Peça", height=300),
                            use_container_width=True)
        with c_ev2:
            st.plotly_chart(go.Figure(go.Bar(x=df_ev['Mês'].apply(lambda x: meses_n[x]), y=df_ev['Valor Total'],
                                             marker_color=COR_EATON)).update_layout(title="Consumo (R$)", height=300),
                            use_container_width=True)
        with c_ev3:
            st.plotly_chart(go.Figure(go.Bar(x=df_ev['Mês'].apply(lambda x: meses_n[x]), y=df_ev['Quantidade'],
                                             marker_color=COR_EATON)).update_layout(title="Produção", height=300),
                            use_container_width=True)

        st.markdown("---")
        st.header("4. Detalhamento e Auditoria")
        c_aud1, c_aud2 = st.columns([1, 4])
        with c_aud1:
            sel_l_aud = st.selectbox("Linha Detalhe", LINHAS_OFICIAIS, key='aud_l')
            sel_a_aud = st.selectbox("Ano Detalhe", sorted(df_s['Ano'].unique()), key='aud_a')
            sel_op_aud = st.selectbox("Operação Detalhe", sorted(df_s[df_s['Linha'] == sel_l_aud]['Operação'].unique()),
                                      key='aud_op')
            sel_m_aud = st.selectbox("Mês Detalhe", range(1, 13), format_func=lambda x: meses_n[x], key='aud_m')
            tipo_m = st.radio("Visualizar por:", ["Valor Total (R$)", "Quantidade"], horizontal=True, key='tipo_aud')
        with c_aud2:
            m_col = 'Valor Total' if "Valor" in tipo_m else 'Qtd'
            ds_aud = \
            df_s[(df_s['Linha'] == sel_l_aud) & (df_s['Operação'] == sel_op_aud) & (df_s['Ano'] == sel_a_aud)].groupby(
                'Mês')[m_col].sum().reset_index()
            df_t = pd.merge(pd.DataFrame({'Mês': range(1, 13)}), ds_aud, on='Mês', how='left').fillna(0)
            st.plotly_chart(px.line(df_t, x=df_t['Mês'].apply(lambda x: meses_n[x]), y=m_col, markers=True,
                                    color_discrete_sequence=[COR_EATON]).update_layout(height=300),
                            use_container_width=True)
            df_aud_final = df_s[
                (df_s['Linha'] == sel_l_aud) & (df_s['Operação'] == sel_op_aud) & (df_s['Ano'] == sel_a_aud) & (
                            df_s['Mês'] == sel_m_aud)]
            if not df_aud_final.empty:
                st.dataframe(df_aud_final[['Data', 'Turno', 'Código', 'Descrição', 'Qtd', 'Valor Unit.',
                                           'Valor Total']].style.format(
                    {'Valor Unit.': 'R$ {:.2f}', 'Valor Total': 'R$ {:.2f}'}), use_container_width=True,
                             hide_index=True)

    # --- PÁGINA 2: ESTOQUE (CORRIGIDA E CONSOLIDADA) ---
    elif st.session_state.pagina == "Estoque":
        st.title("📦 Gestão de Estoque e Auditoria")

        m1, m2, m3, m4 = st.columns(4)

        st.markdown("---")
        col_f1, col_f2 = st.columns([2, 1])
        with col_f1:
            busca = st.text_input("🔍 Buscar Código Eaton ou Descrição para Detalhar", key="busca_est_final")
        with col_f2:
            f_sit = st.multiselect("Filtrar por Situação", df_est['Situação'].unique(), key="sit_est_final")

        df_v = df_est.copy()
        if busca:
            df_v = df_v[df_v['Descrição'].astype(str).str.contains(busca, case=False) |
                        df_v['Código Eaton'].astype(str).str.contains(busca, case=False)]
        if f_sit:
            df_v = df_v[df_v['Situação'].isin(f_sit)]

        m1.metric("Itens Críticos", len(df_v[df_v['Situação'] == "Crítico"]))
        m2.metric("Itens Sem Uso", len(df_v[df_v['Situação'] == "Sem uso"]))
        m3.metric("Saldo Total (Qtd)", f"{int(df_v['Saldo'].sum()):,}".replace(",", "."))
        m4.metric("Valor Imobilizado", f"R$ {fmt_br(df_v['Valor Total'].sum(), 2)}")

        st.dataframe(df_v.style.applymap(lambda x: cor_status(x), subset=['Situação']).format({
            'Valor Unit.': lambda x: f'R$ {fmt_br(x, 2)}', 'Valor Total': lambda x: f'R$ {fmt_br(x, 2)}',
            'Saldo': lambda x: f'{int(x):,}'.replace(',', '.'), 'Uso 60d': lambda x: f'{int(x):,}'.replace(',', '.'),
            'Dias Cobertura': lambda x: f'{int(x)}' if x != "Indeterminado" else "∞"
        }), use_container_width=True, hide_index=True)

        if busca and not df_v.empty:
            st.markdown("---")
            cod_sel = df_v.iloc[0]['Código Eaton']
            st.subheader(f"📑 Rastreabilidade: {cod_sel} - {df_v.iloc[0]['Descrição']}")

            det_c_base = df_s_60d[df_s_60d['Código'] == cod_sel].copy()

            if not det_c_base.empty:
                c_pie, c_tab = st.columns([1, 1.5])
                with c_pie:
                    resumo_linha = det_c_base.groupby('Linha')['Qtd'].sum().reset_index()
                    fig_pie = px.pie(resumo_linha, values='Qtd', names='Linha', hole=0.5, title="Consumo por Linha")
                    fig_pie.update_traces(textinfo='percent+label', marker=dict(colors=px.colors.sequential.Reds_r))
                    st.plotly_chart(fig_pie, use_container_width=True)

                with c_tab:
                    linhas_aud = sorted(det_c_base['Linha'].unique())
                    sel_linha = st.multiselect("Filtrar Tabela por Linha:", options=linhas_aud, default=linhas_aud)
                    det_f = det_c_base[det_c_base['Linha'].isin(sel_linha)]
                    st.dataframe(
                        det_f[['Data', 'Linha', 'Operação', 'Turno', 'Qtd']].sort_values('Data', ascending=False),
                        use_container_width=True, hide_index=True)
            else:
                st.warning("Sem saídas nos últimos 60 dias.")


    # --- PÁGINA 3: SAÍDAS ---
    elif st.session_state.pagina == "Saídas":
        st.title("📑 Registro de Saídas")
        cols = ['Data', 'Linha', 'Operação', 'Turno', 'Código', 'Descrição', 'Qtd', 'Valor Unit.', 'Valor Total']
        st.dataframe(df_s_raw[cols].sort_values('Data', ascending=False), use_container_width=True, hide_index=True)

    # --- PÁGINA 4: PV CONSOLIDADA (SISTEMA DE HIERARQUIA DE ATRASOS) ---
    elif st.session_state.pagina == "Abertura de PV":
        st.title("📋 Controle e Acompanhamento de PVs")

        # 1. CARGA DE PRAZOS DA ABA PCP (CÓDIGO B E TEMPO C)
        try:
            # skiprows=1 assume que os dados começam na linha 2
            df_prazos_pcp = pd.read_excel(caminho, sheet_name="PCP", skiprows=1)
            # Mapeia Código Alcar (Coluna 1) -> Tempo (Coluna 2)
            mapa_prazos = dict(zip(df_prazos_pcp.iloc[:, 1].astype(str).str.strip(), df_prazos_pcp.iloc[:, 2]))
        except Exception as e:
            st.warning(f"Aviso: Aba PCP não carregada. Usando prazos padrão. Erro: {e}")
            mapa_prazos = {}


        # 2. FUNÇÃO DE ESTILO (TEXTO PRETO EM FUNDOS CLAROS E DESTAQUE DE STATUS)
        def estilizacao_final(row):
            styles = [''] * len(row)
            cores_op = {
                'S/OP': 'background-color: #e9ecef; color: black;',
                'MP': 'background-color: #cfe2ff; color: black;',
                'PRENSA': 'background-color: #fff3cd; color: black;',
                'SECAGEM': 'background-color: #e2d9f3; color: black;',
                'QUEIMA': 'background-color: #f8d7da; color: black;',
                'EMBALADO': 'background-color: #d1e7dd; color: black;',
                'PCP': 'background-color: #cff4fc; color: black;'
            }

            # Estilo para Etapa Atual (Coluna OPERAÇÃO)
            if 'OPERAÇÃO' in row.index:
                op_val = str(row['OPERAÇÃO']).strip().upper()
                if op_val in cores_op:
                    styles[row.index.get_loc('OPERAÇÃO')] = cores_op[op_val]
                else:
                    styles[row.index.get_loc('OPERAÇÃO')] = 'color: black;'

            # Estilo para Situação (Atrasos, Transporte e Itens OK)
            if 'SITUAÇÃO' in row.index:
                sit_val = str(row['SITUAÇÃO'])
                idx_sit = row.index.get_loc('SITUAÇÃO')
                if "🚨" in sit_val:
                    styles[idx_sit] = 'background-color: #ff4b4b; color: white; font-weight: bold;'
                elif "🚢" in sit_val:
                    styles[idx_sit] = 'background-color: #007bff; color: white; font-weight: bold;'
                elif "✅" in sit_val:
                    styles[idx_sit] = 'color: #1a7f37; font-weight: bold;'  # Verde escuro
                else:
                    styles[idx_sit] = 'color: black;'

            return styles


        # 3. FUNÇÃO DE CÁLCULO COM HIERARQUIA DE REGRAS
        def calcular_situacao_hierarquica(row, hoje, prazos_dict):
            if pd.isnull(row['DATA']): return "Data pendente"

            dias_contados = (hoje - row['DATA']).days
            status = str(row['OPERAÇÃO']).upper().strip()
            cod_alcar = str(row['ALCAR']).strip()

            # REGRA 1: EXCEÇÃO (QUEIMA E EMBALADO SÃO CONSIDERADOS OK)
            if status in ["QUEIMA", "EMBALADO"]:
                return "✅ Item OK"

            # REGRA 2: PRIORIDADE S/OP (5 DIAS PARA TODOS)
            if status == "S/OP":
                if dias_contados > 5:
                    return f"🚨 ATRASADO S/OP (+{dias_contados}d)"
                return "No Prazo (S/OP)"

            # REGRA 3: ITENS PCP (CONSULTA TABELA DE COMPRAS)
            if status == "PCP" or cod_alcar in prazos_dict:
                prazo_esp = prazos_dict.get(cod_alcar, 30)  # 30 dias se for PCP fora da lista
                if dias_contados > prazo_esp:
                    return f"🚨 ATRASADO PCP (+{dias_contados}d)"
                elif prazo_esp >= 120:
                    return "🚢 EM TRANSPORTE"
                else:
                    return f"PCP: {dias_contados}/{prazo_esp}d"

            # REGRA 4: PRODUÇÃO INTERNA (OUTRAS ETAPAS - 5 DIAS)
            if dias_contados > 5:
                return f"🚨 ATRASADO PROD (+{dias_contados}d)"

            return "Em Processo"


        # 4. PROCESSAMENTO E FILTRAGEM
        df_pv['DATA'] = pd.to_datetime(df_pv['DATA'], errors='coerce')
        hoje_agora = datetime.now()
        df_pv['SITUAÇÃO'] = df_pv.apply(lambda r: calcular_situacao_hierarquica(r, hoje_agora, mapa_prazos), axis=1)

        # 5. LAYOUT SUPERIOR (MÉTRICAS)
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Carteira", len(df_pv))
        m2.metric("Atrasos Críticos", len(df_pv[df_pv['SITUAÇÃO'].str.contains("🚨")]), delta_color="inverse")
        m3.metric("Em Transporte", len(df_pv[df_pv['SITUAÇÃO'].str.contains("🚢")]))
        m4.metric("Itens OK", len(df_pv[df_pv['SITUAÇÃO'] == "✅ Item OK"]))

        # 6. GRÁFICO DE CARGA POR ETAPA
        import plotly.express as px

        df_fig = df_pv['OPERAÇÃO'].value_counts().reset_index()
        df_fig.columns = ['Etapa', 'Qtd']
        ordem_status = ["S/OP", "MP", "PRENSA", "SECAGEM", "QUEIMA", "EMBALADO", "PCP"]
        df_fig['Etapa'] = pd.Categorical(df_fig['Etapa'], categories=ordem_status, ordered=True)
        fig = px.bar(df_fig.sort_values('Etapa'), x='Etapa', y='Qtd', text='Qtd', title="Carga por Etapa")
        fig.update_traces(marker_color='#EF553B', textposition='outside')
        fig.update_layout(height=300, margin=dict(t=50, b=0, l=0, r=0))
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")

        # 7. FILTROS E BUSCA
        f1, f2 = st.columns([1, 2])
        with f1:
            sel_ops = st.multiselect("Filtrar Etapa:", ordem_status,
                                     default=[o for o in ordem_status if o in df_pv['OPERAÇÃO'].unique()])
        with f2:
            busca = st.text_input("🔍 Buscar Código Eaton ou Alcar:")

        # 8. PREPARAÇÃO DA TABELA (REMOÇÃO DE COLUNAS E FORMATAÇÃO DE DATA)
        df_final = df_pv[df_pv['OPERAÇÃO'].isin(sel_ops)].copy()
        if busca:
            mask = (df_final['EATON'].astype(str).str.contains(busca, case=False) |
                    df_final['ALCAR'].astype(str).str.contains(busca, case=False))
            df_final = df_final[mask]

        colunas_remover = ["CONTAGEM CÓDIGO", "PEDIDO", "CONTAGEM", "ITEM", "CONTAGEM - CÓDIGO"]
        cols_visiveis = [c for c in df_final.columns if c.strip().upper() not in colunas_remover]

        df_exibicao = df_final[cols_visiveis].copy()
        if 'DATA' in df_exibicao.columns:
            df_exibicao['DATA'] = df_exibicao['DATA'].dt.strftime('%d/%m/%Y')

        # 9. EXIBIÇÃO FINAL
        st.dataframe(
            df_exibicao.style.apply(estilizacao_final, axis=1),
            use_container_width=True,
            hide_index=True,
            column_config={
                "SITUAÇÃO": st.column_config.TextColumn("Status / Prazo", width="large"),
                "OPERAÇÃO": st.column_config.TextColumn("Etapa Atual", width="medium"),
                "DATA": st.column_config.TextColumn("Fim Oper. Ant.", width="small")
            }
        )
    elif st.session_state.pagina == "Compras":
        st.title("🚀 Planejamento de Abastecimento (Meta 120 Dias)")

        if df_est is not None and df_pv is not None:

            # --- 1. CARREGAMENTO DAS REGRAS DE CARGA ---
            try:
                df_regras = pd.read_excel(caminho, sheet_name="REGRAS_CARGA", skiprows=1)
                df_regras.columns = [str(c).strip().upper() for c in df_regras.columns]
                # Filtra apenas as colunas necessárias para garantir
                df_regras = df_regras[['MÍNIMO', 'MÁXIMO', 'CARGA']].dropna()
            except Exception as e:
                st.error(f"Erro ao ler aba REGRAS_CARGA: {e}")
                df_regras = None


            # --- 2. FUNÇÕES DE APOIO ---
            def extrair_espessura(desc):
                try:
                    partes = str(desc).upper().split('X')
                    if len(partes) >= 2:
                        return float(partes[1].strip())
                except:
                    return 0
                return 0


            def buscar_lote_dinamico(esp, tabela_regras):
                if tabela_regras is None or esp <= 0:
                    return 1  # Padrão caso não encontre regra

                # Procura em qual faixa a espessura se encaixa
                regra = tabela_regras[(esp >= tabela_regras['MÍNIMO']) & (esp <= tabela_regras['MÁXIMO'])]

                if not regra.empty:
                    return int(regra.iloc[0]['CARGA'])
                return 1


            # --- 3. PROCESSAMENTO DOS DADOS ---
            df_pedidos_soma = df_pv.groupby('EATON')['SALDO'].sum().reset_index().rename(
                columns={'EATON': 'Código Eaton', 'SALDO': 'Qtd em Pedido'})
            df_plan = pd.merge(df_est, df_pedidos_soma, on='Código Eaton', how='left').fillna(0)

            # Cálculos de Demanda
            df_plan['Consumo Mensal'] = df_plan['Uso 60d'] / 2
            df_plan['Necessidade 120d'] = df_plan['Consumo Mensal'] * 4
            df_plan['Disponibilidade'] = df_plan['Saldo'] + df_plan['Qtd em Pedido']
            df_plan['Falta_Bruta'] = df_plan['Necessidade 120d'] - df_plan['Disponibilidade']

            # Identificação da Espessura e Lote
            df_plan['Espessura'] = df_plan['Descrição'].apply(extrair_espessura)
            df_plan['Lote_Padrao'] = df_plan['Espessura'].apply(lambda x: buscar_lote_dinamico(x, df_regras))

            # Arredondamento
            import numpy as np


            def aplicar_arredondamento(row):
                if row['Falta_Bruta'] <= 0: return 0
                return int(np.ceil(row['Falta_Bruta'] / row['Lote_Padrao']) * row['Lote_Padrao'])


            df_plan['SUGESTÃO_FINAL'] = df_plan.apply(aplicar_arredondamento, axis=1)

            # --- 4. EXIBIÇÃO ---
            df_sugestao = df_plan[df_plan['SUGESTÃO_FINAL'] > 0].copy()
            df_sugestao['Investimento'] = df_sugestao['SUGESTÃO_FINAL'] * df_sugestao['Valor Unit.']

            c1, c2 = st.columns(2)
            c1.metric("Itens para Reposição", len(df_sugestao))
            c2.metric("Total Investimento", f"R$ {df_sugestao['Investimento'].sum():,.2f}")

            st.dataframe(
                df_sugestao[[
                    'Código Eaton', 'Descrição', 'Espessura', 'Lote_Padrao',
                    'Saldo', 'Qtd em Pedido', 'Falta_Bruta', 'SUGESTÃO_FINAL', 'Investimento'
                ]].sort_values('Investimento', ascending=False).style.format({
                    'Espessura': '{:.1f} mm',
                    'Falta_Bruta': '{:.1f}',
                    'Investimento': 'R$ {:.2f}'
                }),
                use_container_width=True, hide_index=True
            )
# --- BOTÃO DE ATUALIZAÇÃO NO MENU LATERAL ---
with st.sidebar:
    st.markdown("---")
    if st.button("🔄 ATUALIZAR DADOS", use_container_width=True):
        # 1. Limpa o cache de dados e de funções
        st.cache_data.clear()
        st.cache_resource.clear()

        # 2. Força um "reboot" visual do script
        st.toast("Lendo arquivos Excel e recalculando métricas...", icon="⏳")
        st.rerun()
    st.markdown("---")
