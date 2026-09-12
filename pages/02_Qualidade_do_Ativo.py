import streamlit as st
import pandas as pd

@st.cache_data
def carregar_dados():
    return pd.read_csv('data/processed/dataset_limpo.csv')

try:
    df = carregar_dados()
except Exception as e:
    st.error("Erro ao carregar o arquivo: {e}", icon=":material/warning:")
    st.stop()

st.title(":material/payments: Qualidade do Ativo - Limites e Saldo", anchor=False)
st.markdown("Analise de limites de crédito, uso do cartão e volume de transações.")
st.info("Selecione os filtros que quiser à esquerda.", icon=":material/arrow_back:")

# Filtros
st.sidebar.header("Filtros Globais")
df_filtrado = df.copy()

categorias_cartao = ['Azul', 'Prata', 'Ouro', 'Platina']
filtro_cartao = st.sidebar.multiselect("Categoria do Cartão", categorias_cartao)
if filtro_cartao:  
    df_filtrado = df_filtrado[df_filtrado['categoria_cartao'].isin(filtro_cartao)]

generos = list(df['genero'].unique())
filtro_genero = st.sidebar.multiselect("Gênero", generos)
if filtro_genero:
    df_filtrado = df_filtrado[df_filtrado['genero'].isin(filtro_genero)]

rendas = ['Menos de $40 mil', '$40 mil - $60 mil', '$60 mil - $80 mil', '$80 mil - $120 mil', 'Mais de $120 mil']
filtro_renda = st.sidebar.multiselect("Faixa de Renda", rendas)
if filtro_renda: 
    df_filtrado = df_filtrado[df_filtrado['faixa_renda'].isin(filtro_renda)]

estados_civis = ['Solteiro', 'Casado', 'Divorciado']
filtro_estado_civil = st.sidebar.multiselect("Estado Civil", estados_civis)
if filtro_estado_civil:
    df_filtrado = df_filtrado[df_filtrado['estado_civil'].isin(filtro_estado_civil)]

escolaridades = ['Sem escolaridade', 'Ensino Médio', 'Superior Incompleto', 'Graduação', 'Pós-graduação', 'Doutorado']
filtro_escolaridade = st.sidebar.multiselect("Escolaridade", escolaridades)
if filtro_escolaridade:
    df_filtrado = df_filtrado[df_filtrado['escolaridade'].isin(filtro_escolaridade)]

if df_filtrado.empty:
    st.warning("Nenhum cliente encontrado com essa combinação de filtros. Por favor, ajuste as opções na barra lateral.", icon=":material/warning:")
    st.stop()