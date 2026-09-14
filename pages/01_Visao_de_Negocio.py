import streamlit as st
import pandas as pd
import plotly.express as px
from utils import (
    carregar_dados, aplicar_filtros_sidebar, validar_colunas,
    definir_ordem_legenda, botao_download, CORES_STATUS, ORDEM_RENDA
)

try:
    df = carregar_dados()
except Exception as e:
    st.error(f"Erro ao carregar os dados: {e}", icon=":material/warning:")
    st.stop()

validar_colunas(df)

st.title(":material/query_stats: Visão de Negócio - Perfil dos Clientes", anchor=False)
st.markdown("Analise dos indicadores demográficos e o comportamento de cancelamento (*churn*).")
st.info(
    "Selecione os filtros que quiser à esquerda. Ao final da barra lateral, "
    "você encontra o botão para exportar os dados filtrados em CSV.",
    icon=":material/arrow_back:"
)

# Filtragem
df_filtrado = aplicar_filtros_sidebar(df)

if df_filtrado.empty:
    st.warning("Nenhum cliente encontrado com essa combinação de filtros. Por favor, ajuste as opções na barra lateral.", icon=":material/warning:")
    st.stop()

# Resumo de indicadores
st.subheader("Resumo de Indicadores", anchor=False)

col1, col2, col3, col4 = st.columns(4)
total_clientes = len(df_filtrado)
clientes_churn = len(df_filtrado[df_filtrado['status_cliente'] == 'Cancelado'])
taxa_churn = clientes_churn / total_clientes * 100
idade_media = df_filtrado['idade'].mean()

col1.metric("Total de Clientes", f"{total_clientes:,}".replace(',', '.'))
col2.metric("Clientes em Churn", f"{clientes_churn:,}".replace(',', '.'))
col3.metric("Taxa de Churn", f"{taxa_churn:.1f}%")
col4.metric("Idade Média", f"{idade_media:.0f} anos")

st.divider()

# Abas de análise
tab_panorama, tab_perfil_churn = st.tabs(["Panorama de Churn e Renda", "Perfil vs. Churn"])

with tab_panorama:
    col_grafico1, col_grafico2 = st.columns(2)

    # Gráfico 1: Taxa de Churn por Faixa de Renda
    df_renda = df_filtrado.groupby('faixa_renda')['status_cliente'].apply(
        lambda s: (s == 'Cancelado').mean() * 100
    ).reset_index(name='Taxa de Churn (%)')

    ordem_rendas_presentes = [r for r in ORDEM_RENDA if r in df_renda['faixa_renda'].unique()]

    fig_renda = px.bar(
        df_renda,
        x='faixa_renda',
        y='Taxa de Churn (%)',
        title='Taxa de Churn por Faixa de Renda',
        text_auto='.1f',
        color_discrete_sequence=['#1f77b4'],
        labels={'faixa_renda': 'Faixa de Renda'},
        category_orders={'faixa_renda': ordem_rendas_presentes}
    )
    fig_renda.update_traces(textposition='outside')
    col_grafico1.plotly_chart(fig_renda, use_container_width=True)

    # Insight 1 — Pergunta-alvo: "a renda influencia o risco de cancelamento? em qual faixa?"
    pior_faixa = df_renda.loc[df_renda['Taxa de Churn (%)'].idxmax(), 'faixa_renda']
    pior_taxa = df_renda['Taxa de Churn (%)'].max()
    melhor_faixa = df_renda.loc[df_renda['Taxa de Churn (%)'].idxmin(), 'faixa_renda']
    melhor_taxa = df_renda['Taxa de Churn (%)'].min()

    if melhor_taxa > 0:
        razao = pior_taxa / melhor_taxa
        texto_razao = f", quase **{razao:.1f}x maior**"
    else:
        texto_razao = ""

    col_grafico1.caption(
        f":material/insights: **{pior_faixa}** é a faixa de renda com maior risco de churn "
        f"({pior_taxa:.1f}%){texto_razao} do que **{melhor_faixa}** ({melhor_taxa:.1f}%), a mais estável. "
        f"A taxa geral da base filtrada é {taxa_churn:.1f}%."
    )

    # Gráfico 2: Proporção de Churn (Gráfico de Rosca)
    df_status = df_filtrado['status_cliente'].value_counts().reset_index()
    df_status.columns = ['Status', 'Quantidade']

    fig_status = px.pie(
        df_status,
        names='Status',
        values='Quantidade',
        color='Status',
        title='Proporção de Status do Cliente',
        hole=0.4,
        color_discrete_map=CORES_STATUS
    )
    col_grafico2.plotly_chart(fig_status, use_container_width=True)

    # Insight 2 — Pergunta-alvo: "qual a real magnitude do churn nessa base?"
    churn_em_10 = taxa_churn / 10
    col_grafico2.caption(
        f":material/insights: A cada 10 clientes do recorte atual, aproximadamente "
        f"**{churn_em_10:.1f} cancelam** o serviço ({clientes_churn:,} de {total_clientes:,}, ".replace(',', '.')
        + f"{taxa_churn:.1f}%)."
    )

with tab_perfil_churn:
    col_grafico3, col_grafico4 = st.columns(2)

    # Gráfico 3: Distribuição de Idade por Status (Histograma)
    ordem_status, ordem_legenda = definir_ordem_legenda(df_filtrado)

    fig_idade = px.histogram(
        df_filtrado,
        x='idade',
        color='status_cliente',
        title='Distribuição de Idade por Status',
        color_discrete_map=CORES_STATUS,
        labels={'status_cliente': 'Status do Cliente', 'idade': 'Idade'},
        category_orders={'status_cliente': ordem_status}
    )
    fig_idade.update_layout(
        barmode='stack',
        yaxis_title='Quantidade de Clientes',
        legend_traceorder=ordem_legenda
    )
    col_grafico3.plotly_chart(fig_idade, use_container_width=True)

    # Insight 3 — Pergunta-alvo: "existe uma faixa de idade mais propensa a cancelar?"
    idade_media_ativos = df_filtrado.loc[df_filtrado['status_cliente'] == 'Ativo', 'idade'].mean()
    idade_media_cancelados = df_filtrado.loc[df_filtrado['status_cliente'] == 'Cancelado', 'idade'].mean()
    diferenca_idade = idade_media_cancelados - idade_media_ativos

    bins = [0, 30, 40, 50, 60, 150]
    rotulos_bins = ['Até 30', '31-40', '41-50', '51-60', '60+']
    faixa_etaria = pd.cut(df_filtrado['idade'], bins=bins, labels=rotulos_bins)
    churn_por_idade = df_filtrado.groupby(faixa_etaria)['status_cliente'].apply(
        lambda s: (s == 'Cancelado').mean() * 100
    )
    faixa_pior_idade = churn_por_idade.idxmax()
    taxa_pior_idade = churn_por_idade.max()

    if abs(diferenca_idade) < 1:
        frase_idade = (
            f"A idade média é praticamente igual entre ativos ({idade_media_ativos:.0f} anos) "
            f"e cancelados ({idade_media_cancelados:.0f} anos)"
        )
    else:
        direcao_idade = "mais velhos" if diferenca_idade > 0 else "mais jovens"
        frase_idade = (
            f"Clientes cancelados são, em média, **{abs(diferenca_idade):.1f} anos {direcao_idade}** "
            f"que os ativos ({idade_media_cancelados:.0f} vs. {idade_media_ativos:.0f} anos)"
        )

    col_grafico3.caption(
        f":material/insights: {frase_idade}. A faixa etária com maior risco é "
        f"**{faixa_pior_idade} anos** ({taxa_pior_idade:.1f}% de churn)."
    )

    # Gráfico 4: Churn por Categoria de Cartão (Barras Agrupadas)
    df_cartao = df_filtrado.groupby(['categoria_cartao', 'status_cliente']).size().reset_index(name='Quantidade')

    fig_cartao = px.bar(
        df_cartao,
        x='categoria_cartao',
        y='Quantidade',
        color='status_cliente',
        title='Volume por Categoria de Cartão',
        barmode='group',
        text_auto=True,
        color_discrete_map=CORES_STATUS,
        labels={'status_cliente': 'Status do Cliente', 'categoria_cartao': 'Categoria do Cartão'},
        category_orders={'categoria_cartao': ['Azul', 'Prata', 'Ouro', 'Platina']}
    )
    fig_cartao.update_traces(textposition='outside')
    col_grafico4.plotly_chart(fig_cartao, use_container_width=True)

    # Insight 4 — Pergunta-alvo: "alguma categoria de cartão perde clientes desproporcionalmente?"
    df_taxa_cartao = df_filtrado.groupby('categoria_cartao')['status_cliente'].apply(
        lambda s: (s == 'Cancelado').mean() * 100
    )
    pior_cartao = df_taxa_cartao.idxmax()
    melhor_cartao = df_taxa_cartao.idxmin()

    col_grafico4.caption(
        f":material/insights: **{pior_cartao}** tem a maior taxa de churn "
        f"({df_taxa_cartao.max():.1f}%); **{melhor_cartao}** tem a menor "
        f"({df_taxa_cartao.min():.1f}%)."
    )