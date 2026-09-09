import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(
    page_title="Visão de Negócio",
    page_icon="📈",
    layout="wide"
)

@st.cache_data
def carregar_dados():
    return pd.read_csv('data/dataset_limpo.csv')

try:
    df = carregar_dados()
except FileNotFoundError:
    st.error("Arquivo 'data/dataset_limpo.csv' não encontrado. Verifique se o caminho do arquivo está correto.")
    st.stop()

st.title("📈 Visão de Negócio - Perfil dos Clientes")
st.markdown("Analise os indicadores demográficos e o comportamento de cancelamento (churn).")

# Barra lateral -> filtros
st.sidebar.header("Filtros Globais")

    # Categoria do cartão
categorias_cartao = ['Todos'] + list(df['categoria_cartao'].unique())
filtro_cartao = st.sidebar.selectbox("Categoria do Cartão", categorias_cartao)

    # Filtro de gênero
generos = ['Todos'] + list(df['genero'].unique())
filtro_genero = st.sidebar.selectbox("Gênero", generos)

# Aplicando os filtros ao dataframe
df_filtrado = df.copy()

if filtro_cartao != 'Todos':
    df_filtrado = df_filtrado[df_filtrado['categoria_cartao'] == filtro_cartao]

if filtro_genero != 'Todos':
    df_filtrado = df_filtrado[df_filtrado['genero'] == filtro_genero]

# --- PAINEL DE KPIS ---
col1, col2, col3, col4 = st.columns(4)

total_clientes = len(df_filtrado)
clientes_churn = len(df_filtrado[df_filtrado['status_cliente'].str.contains('Attrited', case=False, na=False)])
taxa_churn = (clientes_churn / total_clientes * 100) if total_clientes > 0 else 0
idade_media = df_filtrado['idade'].mean() if total_clientes > 0 else 0

col1.metric("Total de Clientes", f"{total_clientes:,}")
col2.metric("Clientes em Churn", f"{clientes_churn:,}")
col3.metric("Taxa de Churn", f"{taxa_churn:.1f}%")
col4.metric("Idade Média", f"{idade_media:.1f} anos")

st.divider()

# --- GRÁFICOS ---
col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    st.subheader("Proporção de Status do Cliente")
    fig_status = px.pie(
        df_filtrado, 
        names='status_cliente', 
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    st.plotly_chart(fig_status, use_container_width=True)

with col_graf2:
    st.subheader("Distribuição por Escolaridade")
    fig_esc = px.histogram(
        df_filtrado, 
        x='escolaridade', 
        color='status_cliente',
        barmode='group',
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig_esc.update_layout(xaxis_title="Escolaridade", yaxis_title="Quantidade")
    st.plotly_chart(fig_esc, use_container_width=True)

col_graf3, col_graf4 = st.columns(2)

with col_graf3:
    st.subheader("Churn por Faixa Etária")
    fig_idade = px.histogram(
        df_filtrado, 
        x='idade', 
        color='status_cliente', 
        nbins=15,
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig_idade.update_layout(xaxis_title="Idade", yaxis_title="Quantidade")
    st.plotly_chart(fig_idade, use_container_width=True)

with col_graf4:
    st.subheader("Distribuição por Faixa de Renda")
    fig_renda = px.histogram(
        df_filtrado, 
        x='faixa_renda', 
        color='status_cliente',
        barmode='group',
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig_renda.update_layout(xaxis_title="Faixa de Renda", yaxis_title="Quantidade")
    st.plotly_chart(fig_renda, use_container_width=True)