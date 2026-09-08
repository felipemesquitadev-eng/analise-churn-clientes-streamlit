import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Gestão de Cartões - Data Assets",
    page_icon="💳",
    layout="wide"
)

@st.cache_data
def carregar_dados():
    df = pd.read_csv("[nome]") 
    return df

df = carregar_dados()

st.title("💳 Visão de Portfólio e Churn de Cartões")
st.markdown("Monitoramento de **Ativos de Dados** e comportamento de clientes.")
st.divider()


aba_negocio, aba_qualidade, aba_simulador = st.tabs([
    "📊 Visão de Negócio", 
    "🔍 Qualidade do Ativo", 
    "⚙️ Simulador de Perfil"
])

with aba_negocio:
    st.subheader("Base de Clientes Bruta")
    st.dataframe(df.head(100), use_container_width=True)

with aba_qualidade:
    st.subheader("Governança e Saúde dos Dados")
    st.info("Em construção: Métricas de nulos e validação de tipos de dados.")

with aba_simulador:
    st.subheader("Simulação de Risco de Cancelamento")
    st.info("Em construção: Formulário interativo.")