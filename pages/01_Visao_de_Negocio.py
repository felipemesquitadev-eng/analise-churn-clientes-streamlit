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
    return pd.read_csv('data/processed/dataset_limpo.csv')

try:
    df = carregar_dados()
except Exception as e:
    st.error(f"Erro ao carregar os dados: {e}")
    st.stop()

st.title("📈 Visão de Negócio - Perfil dos Clientes")
st.markdown("Analise os indicadores demográficos e o comportamento de cancelamento (churn).")
