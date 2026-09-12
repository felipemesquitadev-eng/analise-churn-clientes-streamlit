import streamlit as st

st.set_page_config(
    page_title="Análise e Previsão de Churn",
    page_icon=':material/credit_card_gear:',
    layout="wide"
)

def home_page():
    st.title(":material/credit_card_gear: Análise e Previsão de Churn de Cartões de Crédito", anchor=False)

    st.write("""
    Bem-vindo ao **Dashboard Executivo de Análise de Clientes**. 

    Este aplicativo interativo foi desenvolvido para explorar a base de dados de clientes de cartões de crédito, entender os fatores que levam ao cancelamento do serviço (*churn*) e simular o risco de evasão de novos perfis.
    """)

    st.subheader("Navegação", anchor=False)
    st.markdown("""
    Utilize a barra lateral à esquerda para acessar as diferentes visões do projeto:

    *   **Visão de Negócio:** Explore os perfis demográficos e a distribuição geral da base.
    *   **Qualidade do Ativo:** Analise limites de crédito, volumetria de transações e comportamento financeiro.
    *   **Simulador de Churn:** Uma ferramenta interativa para testar perfis de clientes contra o modelo preditivo.
    """)

    st.info("Abra o menu lateral clicando no ícone no canto superior esquerdo para começar.", icon=":material/arrow_back:")

pagina_inicial = st.Page(
    home_page,
    title="Página Inicial", 
    icon=":material/home:", 
    default=True
)
visao_negocio = st.Page(
    "pages/01_Visao_de_Negocio.py", 
    title="Visão de Negócio", 
    icon=":material/query_stats:"
)
qualidade_ativo = st.Page(
    "pages/02_Qualidade_do_Ativo.py", 
    title="Qualidade do Ativo", 
    icon=":material/payments:"
)
simulador = st.Page(
    "pages/03_Simulador_de_Churn.py", 
    title="Simulador de Churn", 
    icon=":material/manufacturing:"
)

pg = st.navigation({
    "Introdução": [pagina_inicial],
    "Painéis": [visao_negocio, qualidade_ativo, simulador]
})

pg.run()

st.divider()
st.caption("""
**Painel de Análise e Previsão de Churn** | 2026  
Desenvolvido por:  
**Felipe Scarpin Mesquita** • [LinkedIn](https://www.linkedin.com/in/felipe-scarpin-mesquita-b8a8893aa/) • [GitHub](https://github.com/felipemesquitadev-eng)  
**Alana Generoso Fidélis da Cruz** • [LinkedIn](https://www.linkedin.com/in/alanageneroso05/) • [GitHub](https://github.com/alanageneroso05)  
*Fonte dos dados: Kaggle (Credit Card Customers) • Projeto demonstrativo para portfólio.*
""")