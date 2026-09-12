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

st.title(":material/payments: Qualidade do Ativo")