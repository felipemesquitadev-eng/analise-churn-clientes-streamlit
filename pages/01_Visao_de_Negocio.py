import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Visão de Negócio",
    page_icon="📈",
    layout="wide"
)

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

categorias_cartao = ['Todos'] + list(df['categoria_cartao'].unique())
filtro_cartao = st.sidebar.multiselect("Categoria do Cartão", categorias_cartao)
if filtro_cartao != 'Todos':
    df_filtrado = df_filtrado[df_filtrado['categoria_cartao'] == filtro_cartao]

generos = ['Todos'] + list(df['genero'].unique())
filtro_genero = st.sidebar.multiselect("Gênero", generos)
if filtro_genero != 'Todos':
    df_filtrado = df_filtrado[df_filtrado['genero'] == filtro_genero]

rendas = list(df['faixa_renda'].unique())
filtro_renda = st.sidebar.multiselect("Faixa de Renda", rendas)
if filtro_renda:  # Verifica se a lista não está vazia
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