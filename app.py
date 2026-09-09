import streamlit as st

st.set_page_config(
    page_title="Previsão de Churn",
    page_icon="💳",
    layout="centered"
)

# 2. Título Principal
st.title("💳 Previsão e Análise de Churn de Cartões de Crédito")

st.write("""
Bem-vindo ao **Dashboard Executivo de Análise de Clientes**. 

Este site[aplicativo] interativo foi desenvolvido para explorar a base de dados de clientes de cartões de crédito, entender os fatores que levam ao cancelamento do serviço (*churn*) e simular o risco de evasão de novos perfis.
""")

st.markdown("### 🧭 Navegação")
st.markdown("""
Utilize a barra lateral à esquerda para acessar as diferentes visões do projeto:

*   **📈 01. Visão de Negócio:** Explore os perfis demográficos e a distribuição geral da base.
*   **📊 02. Qualidade do Ativo:** Analise limites de crédito, volumetria de transações e comportamento financeiro.
*   **⚙️ 03. Simulador de Churn:** Uma ferramenta interativa para testar perfis de clientes contra o modelo preditivo.
""")

st.info("👈 Abra o menu lateral clicando no ícone no canto superior esquerdo para começar.")