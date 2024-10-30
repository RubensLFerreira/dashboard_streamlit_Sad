import streamlit as st
import pandas as pd


def filtro_dinamico(dataframes):
    # Seleção de ano e coluna para análise
    selected_year = st.selectbox("Selecione o ano para análise:", ["2020", "2024"])
    df = dataframes[selected_year]

    st.subheader(f"Resumo Geral das Eleições de {selected_year}")

    # Filtro dinâmico de coluna
    selected_column = st.selectbox("Selecione a coluna para análise:", df.columns)
    if selected_column:
        column_data = df[selected_column].value_counts().reset_index()
        column_data.columns = [selected_column, "Frequência"]

        # Exibir valores únicos e frequência de cada valor na coluna selecionada
        st.write(f"Distribuição de valores para a coluna **{selected_column}**:")
        st.table(column_data)

    # Exibição dos resumos de cada ano
    total_candidatos = df["SQ_CANDIDATO"].nunique()
    candidatos_eleitos = df[df["DS_SIT_TOT_TURNO"] == "ELEITO"][
        "SQ_CANDIDATO"
    ].nunique()
    total_municipios = df["NM_MUNICIPIO"].nunique()
    eleitos_por_partido = (
        df[df["DS_SIT_TOT_TURNO"] == "ELEITO"]
        .groupby("SG_PARTIDO")["SQ_CANDIDATO"]
        .nunique()
    )

    # Criar tabela para exibir os resultados
    tabela_resultados = pd.DataFrame(
        {
            "Total de Candidatos Inscritos": [total_candidatos],
            "Candidatos Eleitos": [candidatos_eleitos],
            "Total de Municípios": [total_municipios],
        }
    )

    # Exibir a tabela de resumo
    st.subheader(f"Estatísticas Resumidas das Eleições de {selected_year}")
    st.table(tabela_resultados)

    # Exibir candidatos eleitos por partido
    st.write(f"Número de Candidatos Eleitos por Partido em {selected_year}")
    st.table(eleitos_por_partido)
