import streamlit as st

st.set_page_config(
    page_title="Dashboard de Churn",
    page_icon="💳",
    layout="wide"
)

st.title("💳 Previsão e Análise de Churn - Cartões de Crédito")

st.markdown("""
Bem-vindo ao painel interativo de análise de clientes! 

Utilize o menu lateral para navegar entre as seções:
* **01 - Visão de Negócio:** Analise o perfil demográfico e as métricas gerais da base de clientes.
* **02 - Qualidade do Ativo:** Acompanhe o comportamento financeiro, limites de crédito, saldos e transações.
* **03 - Simulador de Churn:** Insira os dados de um cliente para prever a probabilidade de cancelamento do cartão.
""")

st.info("👈 Selecione uma página no menu lateral para começar.")