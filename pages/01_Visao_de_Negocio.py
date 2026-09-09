import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def carregar_dados():
    return pd.read_csv('data/processed/dataset_limpo.csv')

try:
    df = carregar_dados()
except Exception as e:
    st.error(f"Erro ao carregar os dados: {e}")
    st.stop()

st.title("📈 Visão de Negócio - Perfil dos Clientes")
st.markdown("Analise os indicadores demográficos e o comportamento de cancelamento (*churn*).")
st.info("👈 Selecione os filtros que quiser à esquerda.")

# Filtros
st.sidebar.header("Filtros Globais")
df_filtrado = df.copy()

categorias_cartao = list(df['categoria_cartao'].unique())
filtro_cartao = st.sidebar.multiselect("Categoria do Cartão", categorias_cartao)
if filtro_cartao:  # Se a lista não estiver vazia
    df_filtrado = df_filtrado[df_filtrado['categoria_cartao'].isin(filtro_cartao)]

generos = list(df['genero'].unique())
filtro_genero = st.sidebar.multiselect("Gênero", generos)
if filtro_genero:
    df_filtrado = df_filtrado[df_filtrado['genero'].isin(filtro_genero)]

rendas = list(df['faixa_renda'].unique())
filtro_renda = st.sidebar.multiselect("Faixa de Renda", rendas)
if filtro_renda: 
    df_filtrado = df_filtrado[df_filtrado['faixa_renda'].isin(filtro_renda)]

estados_civis = list(df['estado_civil'].unique())
filtro_estado_civil = st.sidebar.multiselect("Estado Civil", estados_civis)
if filtro_estado_civil:
    df_filtrado = df_filtrado[df_filtrado['estado_civil'].isin(filtro_estado_civil)]

escolaridades = list(df['escolaridade'].unique())
filtro_escolaridade = st.sidebar.multiselect("Escolaridade", escolaridades)
if filtro_escolaridade:
    df_filtrado = df_filtrado[df_filtrado['escolaridade'].isin(filtro_escolaridade)]

# Resumo de indicadores
st.subheader("Resumo de Indicadores", anchor=False)

col1, col2, col3, col4 = st.columns(4)
total_clientes = len(df_filtrado)

clientes_churn = len(df_filtrado[df_filtrado['status_cliente'] == 'Cancelado'])
taxa_churn = (clientes_churn / total_clientes * 100) if total_clientes > 0 else 0
idade_media = df_filtrado['idade'].mean() if total_clientes > 0 else 0

col1.metric("Total de Clientes", f"{total_clientes:,}".replace(',', '.'))
col2.metric("Clientes em Churn", f"{clientes_churn:,}".replace(',', '.'))
col3.metric("Taxa de Churn", f"{taxa_churn:.1f}%")
col4.metric("Idade Média", f"{idade_media:.0f} anos")

st.divider()

# Gráficos
st.subheader("Análise Demográfica", anchor=False)
col_grafico1, col_grafico2 = st.columns(2)

# Gráfico 1: Clientes por Faixa de Renda (Gráfico de Barras)
df_renda = df_filtrado['faixa_renda'].value_counts().reset_index()
df_renda.columns = ['Faixa de Renda', 'Quantidade']

fig_renda = px.bar(
    df_renda, 
    x='Faixa de Renda', 
    y='Quantidade', 
    title='Distribuição por Faixa de Renda',
    text_auto=True,
    color_discrete_sequence=['#1f77b4']
)

col_grafico1.plotly_chart(fig_renda, use_container_width=True)


# GRÁFICO 2: Proporção de Churn (Gráfico de Rosca)
df_status = df_filtrado['status_cliente'].value_counts().reset_index()
df_status.columns = ['Status', 'Quantidade']

fig_status = px.pie(
    df_status, 
    names='Status', 
    values='Quantidade', 
    title='Proporção de Status do Cliente',
    hole=0.4,
    color_discrete_sequence=['#2ca02c', '#d62728']
)
col_grafico2.plotly_chart(fig_status, use_container_width=True)