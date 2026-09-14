import streamlit as st
import pandas as pd
import plotly.express as px

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

st.subheader("Métricas Financeiras da Carteira", anchor=False)

#Painel de KPIs
def formata_moeda(valor):
    return f"US$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
def formata_percentual(valor):
    return f"{valor:.2f}%".replace(".", ",")

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

limite_medio = df_filtrado['limite_credito'].mean()
rotativo_medio = df_filtrado['saldo_rotativo'].mean()
transacao_media = df_filtrado['valor_total_transacoes'].mean()
utilizacao_media = df_filtrado['taxa_utilizacao_credito'].mean() * 100

kpi1.metric("Limite Médio", formata_moeda(limite_medio))
kpi2.metric("Rotativo Médio", formata_moeda(rotativo_medio))
kpi3.metric("Transação Média", formata_moeda(transacao_media))
kpi4.metric("Uso Médio de Crédito", formata_percentual(utilizacao_media))

st.divider()

col_grafico1, col_grafico2 = st.columns(2)

with col_grafico1:
    st.markdown("**Distribuição de Limite de Crédito**")
    
    fig_limite = px.box(
        df_filtrado, 
        x='status_cliente', 
        y='limite_credito', 
        color='status_cliente',
        color_discrete_map={'Ativo': '#2ca02c', 'Cancelado': '#d62728'},
        category_orders={'status_cliente': ['Ativo', 'Cancelado']},
        labels={'status_cliente': 'Status', 'limite_credito': 'Limite de Crédito ($)'}
    )
    fig_limite.update_layout(
        showlegend=False,
        margin=dict(l=0, r=0, t=30, b=0),
        height=350
    )
    st.plotly_chart(fig_limite, use_container_width=True)

with col_grafico2:
    st.markdown("**Taxa de Uso do Crédito por Categoria**")
    
    df_uso = df_filtrado.groupby(['categoria_cartao', 'status_cliente'])['taxa_utilizacao_credito'].mean().reset_index()
    df_uso['taxa_utilizacao_credito'] = df_uso['taxa_utilizacao_credito'] * 100 # %
    
    ordem_cartoes = ['Azul', 'Prata', 'Ouro', 'Platina']
    
    fig_uso = px.bar(
        df_uso, 
        x='categoria_cartao', 
        y='taxa_utilizacao_credito', 
        color='status_cliente',
        barmode='group',
        color_discrete_map={'Ativo': '#2ca02c', 'Cancelado': '#d62728'},
        category_orders={
            'status_cliente': ['Ativo', 'Cancelado'],
            'categoria_cartao': ordem_cartoes
        },
        text_auto='.1f',
        labels={'categoria_cartao': 'Categoria', 'taxa_utilizacao_credito': 'Uso do Limite (%)', 'status_cliente': 'Status'}
    )
    fig_uso.update_traces(textposition='outside')
    fig_uso.update_layout(
        margin=dict(l=0, r=0, t=30, b=0),
        height=350,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_uso, use_container_width=True)