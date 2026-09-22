# utils.py
import streamlit as st
import pandas as pd
import os

CAMINHO_DADOS = 'data/processed/dataset_limpo.csv'
COLUNAS_ESPERADAS = [
    'categoria_cartao', 'genero', 'faixa_renda', 'estado_civil', 'escolaridade',
    'status_cliente', 'idade', 'limite_credito', 'saldo_rotativo',
    'valor_total_transacoes', 'taxa_utilizacao_credito', 'qtd_total_transacoes'
]
CORES_STATUS = {'Ativo': '#2ca02c', 'Cancelado': '#d62728'}
ORDEM_ESCOLARIDADE = ['Sem escolaridade', 'Ensino Médio', 'Superior Incompleto',
                       'Graduação', 'Pós-graduação', 'Doutorado', 'Desconhecido']
ORDEM_RENDA = ['Menos de $40 mil', '$40 mil - $60 mil', '$60 mil - $80 mil',
               '$80 mil - $120 mil', 'Mais de $120 mil', 'Desconhecido']
ORDEM_CARTAO = ['Azul', 'Prata', 'Ouro', 'Platina']
ORDEM_ESTADO_CIVIL = ['Solteiro', 'Casado', 'Divorciado', 'Desconhecido']

@st.cache_data
def carregar_dados(caminho: str = CAMINHO_DADOS) -> pd.DataFrame:
    mtime = os.path.getmtime(caminho)
    return _ler_csv(caminho, mtime)

@st.cache_data
def _ler_csv(caminho: str, _mtime: float) -> pd.DataFrame:
    return pd.read_csv(caminho)

def validar_colunas(df: pd.DataFrame, colunas_esperadas: list = COLUNAS_ESPERADAS) -> None:
    faltantes = [c for c in colunas_esperadas if c not in df.columns]
    if faltantes:
        st.error(
            f"O dataset está incompleto. Colunas ausentes: {', '.join(faltantes)}",
            icon=":material/warning:"
        )
        st.stop()

def _ordem_presente(ordem_completa: list, valores_presentes) -> list:
    presentes = set(valores_presentes)
    return [v for v in ordem_completa if v in presentes]

def aplicar_filtros_sidebar(df: pd.DataFrame) -> pd.DataFrame:
    st.sidebar.header("Filtros Globais")
    df_filtrado = df.copy()

    filtros = {
        'categoria_cartao': _ordem_presente(ORDEM_CARTAO, df['categoria_cartao'].unique()),
        'genero': sorted(df['genero'].unique()),
        'faixa_renda': _ordem_presente(ORDEM_RENDA, df['faixa_renda'].unique()),
        'estado_civil': _ordem_presente(ORDEM_ESTADO_CIVIL, df['estado_civil'].unique()),
        'escolaridade': _ordem_presente(ORDEM_ESCOLARIDADE, df['escolaridade'].unique()),
    }
    labels = {
        'categoria_cartao': "Categoria do Cartão",
        'genero': "Gênero",
        'faixa_renda': "Faixa de Renda",
        'estado_civil': "Estado Civil",
        'escolaridade': "Escolaridade",
    }

    for coluna, opcoes in filtros.items():
        chave = f"filtro_{coluna}"

        selecionado = st.sidebar.multiselect(
            labels[coluna],
            options=opcoes,
            key=chave
        )
        if selecionado:
            df_filtrado = df_filtrado[df_filtrado[coluna].isin(selecionado)]

    return df_filtrado

def definir_ordem_legenda(df: pd.DataFrame, coluna_status: str = 'status_cliente',
                           valor_top: str = 'Cancelado', valor_bottom: str = 'Ativo'):
    contagem = df[coluna_status].value_counts()
    qtd_top = contagem.get(valor_top, 0)
    qtd_bottom = contagem.get(valor_bottom, 0)

    if qtd_bottom >= qtd_top:
        ordem_categorias = [valor_top, valor_bottom]
        ordem_legenda = 'reversed'
    else:
        ordem_categorias = [valor_bottom, valor_top]
        ordem_legenda = 'normal'

    return ordem_categorias, ordem_legenda

def formata_moeda(valor: float) -> str:
    if pd.isna(valor):
        return r"US\$ 0,00"
    valor_formatado = f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"US\\$ {valor_formatado}"

def formata_percentual(valor: float) -> str:
    return f"{valor:.2f}%".replace(".", ",")

def botao_download(df: pd.DataFrame, nome_arquivo: str,
                    label: str = "Exportar dados filtrados (.csv)",
                    container=None) -> None:
    """Adiciona um botão de download do dataframe filtrado, em CSV.
    'container' permite renderizar em st.sidebar, dentro de uma coluna, etc.
    Se None, renderiza no fluxo normal (corpo da página)."""
    destino = container if container is not None else st
    destino.caption("Exporte o recorte atual dos dados:")
    csv = df.to_csv(index=False, sep=';', decimal=',').encode('utf-8-sig')
    destino.download_button(
        label=label,
        data=csv,
        file_name=nome_arquivo,
        mime="text/csv",
        icon=":material/download:"
    )