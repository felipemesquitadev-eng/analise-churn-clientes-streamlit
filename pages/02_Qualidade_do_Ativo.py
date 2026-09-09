import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Qualidade do Ativo",
    page_icon="📊",
    layout="wide")

st.title("📊 Qualidade do Ativo")

@st.cache_data
def carregar_dados():
    return pd.read_csv('data/processed/dataset_limpo.csv')

try:
    df = carregar_dados()
except Exception as e:
    st.error("Erro ao carregar o arquivo: {e}")
    st.stop()