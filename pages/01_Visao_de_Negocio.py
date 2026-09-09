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
st.markdown("Analise os indicadores demográficos e o comportamento de cancelamento (churn).")

st.sidebar.header("Filtros Globais")

categorias_cartao = ['Todos'] + list(df['categoria_cartao'].unique())
filtro_cartao = st.sidebar.selectbox("Categoria do Cartão", categorias_cartao)

generos = ['Todos'] + list(df['genero'].unique())
filtro_genero = st.sidebar.selectbox("Gênero", generos)

df_filtrado = df.copy()

if filtro_cartao != 'Todos':
    df_filtrado = df_filtrado[df_filtrado['categoria_cartao'] == filtro_cartao]

if filtro_genero != 'Todos':
    df_filtrado = df_filtrado[df_filtrado['genero'] == filtro_genero]