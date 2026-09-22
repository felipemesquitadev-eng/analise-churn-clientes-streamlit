import streamlit as st
import pandas as pd
import plotly.express as px
from utils import (
    carregar_dados, aplicar_filtros_sidebar, validar_colunas,
    formata_moeda, formata_percentual, botao_download, CORES_STATUS
)

try:
    df = carregar_dados()
except Exception as e:
    st.error(f"Erro ao carregar os dados: {e}", icon=":material/warning:")
    st.stop()

validar_colunas(df)

st.title(":material/payments: Qualidade do Ativo - Limites e Saldo", anchor=False)
st.markdown("Analise de limites de crédito, uso do cartão e volume de transações.")
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
botao_download(df_filtrado, nome_arquivo="clientes_qualidade_ativo.csv", container=st.sidebar)

st.subheader("Métricas Financeiras da Carteira", anchor=False)

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

tab_limites, tab_transacoes = st.tabs(["Limites e Utilização", "Transações"])

with tab_limites:
    col_grafico1, col_grafico2 = st.columns(2)

    with col_grafico1:
        st.markdown("**Distribuição de Limite de Crédito**")

        tem_flag_suspeito = 'limite_suspeito' in df_filtrado.columns
        excluir_suspeitos = False
        if tem_flag_suspeito:
            excluir_suspeitos = st.checkbox(
                "Excluir valores de limite atipicamente repetidos",
                value=False,
                help="Remove da visualização clientes com limite de crédito idêntico a "
                     "valores que se repetem de forma estatisticamente improvável no dataset."
            )

        df_grafico_limite = df_filtrado
        if excluir_suspeitos:
            df_grafico_limite = df_filtrado[~df_filtrado['limite_suspeito']]

        fig_limite = px.box(
            df_grafico_limite,
            x='status_cliente',
            y='limite_credito',
            color='status_cliente',
            color_discrete_map=CORES_STATUS,
            category_orders={'status_cliente': ['Ativo', 'Cancelado']},
            labels={'status_cliente': 'Status', 'limite_credito': 'Limite de Crédito ($)'}
        )
        fig_limite.update_layout(
            showlegend=False,
            margin=dict(l=0, r=0, t=30, b=0),
            height=350
        )
        st.plotly_chart(fig_limite, use_container_width=True)

        if tem_flag_suspeito and df_grafico_limite.empty:
            st.warning("Nenhum cliente restante após excluir os valores suspeitos.", icon=":material/warning:")

        # Insight — Pergunta-alvo: "quem cancela tem um perfil de limite diferente?"
        if not df_grafico_limite.empty:
            limite_cancelados = df_grafico_limite.loc[df_grafico_limite['status_cliente'] == 'Cancelado', 'limite_credito'].mean()
            limite_ativos = df_grafico_limite.loc[df_grafico_limite['status_cliente'] == 'Ativo', 'limite_credito'].mean()
            if pd.notna(limite_cancelados) and pd.notna(limite_ativos) and limite_ativos > 0:
                diferenca_limite = ((limite_cancelados - limite_ativos) / limite_ativos) * 100
                direcao_limite = "maior" if diferenca_limite > 0 else "menor"
                st.caption(
                    f":material/insights: Clientes cancelados têm limite médio "
                    f"**{abs(diferenca_limite):.1f}% {direcao_limite}** ({formata_moeda(limite_cancelados)}) "
                    f"do que clientes ativos ({formata_moeda(limite_ativos)})."
                )

    with col_grafico2:
        st.markdown("**Taxa Média de Uso do Crédito por Categoria**")

        df_uso = df_filtrado.groupby(['categoria_cartao', 'status_cliente'])['taxa_utilizacao_credito'].mean().reset_index()
        df_uso['taxa_utilizacao_credito'] = df_uso['taxa_utilizacao_credito'] * 100

        ordem_cartoes = ['Azul', 'Prata', 'Ouro', 'Platina']

        fig_uso = px.bar(
            df_uso,
            x='categoria_cartao',
            y='taxa_utilizacao_credito',
            color='status_cliente',
            barmode='group',
            color_discrete_map=CORES_STATUS,
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

        # Insight — Pergunta-alvo: "clientes que cancelam usam o crédito de forma diferente?"
        uso_cancelados = df_filtrado.loc[df_filtrado['status_cliente'] == 'Cancelado', 'taxa_utilizacao_credito'].mean() * 100
        uso_ativos = df_filtrado.loc[df_filtrado['status_cliente'] == 'Ativo', 'taxa_utilizacao_credito'].mean() * 100
        if pd.notna(uso_cancelados) and pd.notna(uso_ativos):
            diferenca_uso = uso_cancelados - uso_ativos
            direcao_uso = "mais" if diferenca_uso > 0 else "menos"
            st.caption(
                f":material/insights: Clientes cancelados usam, em média, "
                f"**{abs(diferenca_uso):.1f} pontos percentuais {direcao_uso}** do limite "
                f"({uso_cancelados:.1f}% vs. {uso_ativos:.1f}% dos ativos)."
            )

with tab_transacoes:
    st.markdown("**Comportamento de Compras: Volume vs. Valor Transacionado**")

    fig_transacoes = px.scatter(
        df_filtrado,
        x='qtd_total_transacoes',
        y='valor_total_transacoes',
        color='status_cliente',
        color_discrete_map=CORES_STATUS,
        opacity=0.6,
        labels={
            'qtd_total_transacoes': 'Quantidade de Transações (Últimos 12 meses)',
            'valor_total_transacoes': 'Valor Total Transacionado ($)',
            'status_cliente': 'Status'
        }
    )
    fig_transacoes.update_layout(
        margin=dict(l=0, r=0, t=10, b=0),
        height=450,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_transacoes, use_container_width=True)

    # Insight — Pergunta-alvo: "quem cancela transaciona menos, tanto em volume quanto em valor?"
    qtd_cancelados = df_filtrado.loc[df_filtrado['status_cliente'] == 'Cancelado', 'qtd_total_transacoes'].mean()
    qtd_ativos = df_filtrado.loc[df_filtrado['status_cliente'] == 'Ativo', 'qtd_total_transacoes'].mean()
    valor_cancelados = df_filtrado.loc[df_filtrado['status_cliente'] == 'Cancelado', 'valor_total_transacoes'].mean()
    valor_ativos = df_filtrado.loc[df_filtrado['status_cliente'] == 'Ativo', 'valor_total_transacoes'].mean()

    if pd.notna(qtd_cancelados) and pd.notna(qtd_ativos) and qtd_ativos > 0 and valor_ativos > 0:
        queda_qtd = (1 - qtd_cancelados / qtd_ativos) * 100
        queda_valor = (1 - valor_cancelados / valor_ativos) * 100
        st.caption(
            f":material/insights: Clientes cancelados realizam **{queda_qtd:.0f}% menos transações** "
            f"({qtd_cancelados:.0f} vs. {qtd_ativos:.0f}) e movimentam **{queda_valor:.0f}% menos valor** "
            f"({formata_moeda(valor_cancelados)} vs. {formata_moeda(valor_ativos)}) do que clientes ativos."
        )