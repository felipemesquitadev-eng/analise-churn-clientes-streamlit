import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Visão de Negócio",
    page_icon="📈",
    layout="wide")

st.title("📈 Visão de Negócio")

@st.cache_data
def carregar_dados():
    return pd.read_csv('data/dataset_limpo.csv')

try:
    df = carregar_dados()
    st.success("Dados carregados com sucesso!")
    st.dataframe(df.head())
    
except FileNotFoundError:
    st.error("Arquivo de dados não encontrado. Verifique se o 'dataset_limpo.csv' está na pasta 'data/'.")