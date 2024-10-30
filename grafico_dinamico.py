import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


def grafico_dinamico(dataframes):
    # Separar os DataFrames de 2020 e 2024
    df_2020 = dataframes["2020"]
    df_2024 = dataframes["2024"]

    # 1. Gráfico de Barras - Total de Candidatos Inscritos e Eleitos por Ano
    st.subheader("Total de Candidatos Inscritos e Eleitos por Ano")
    candidatos_inscritos = [
        df_2020["SQ_CANDIDATO"].nunique(),
        df_2024["SQ_CANDIDATO"].nunique(),
    ]
    candidatos_eleitos = [
        df_2020[df_2020["DS_SIT_TOT_TURNO"] == "ELEITO"]["SQ_CANDIDATO"].nunique(),
        df_2024[df_2024["DS_SIT_TOT_TURNO"] == "ELEITO"]["SQ_CANDIDATO"].nunique(),
    ]

    fig, ax = plt.subplots()
    ax.bar(["2020", "2024"], candidatos_inscritos, label="Inscritos", color="skyblue")
    ax.bar(["2020", "2024"], candidatos_eleitos, label="Eleitos", color="salmon")
    ax.set_ylabel("Número de Candidatos")
    ax.legend()
    st.pyplot(fig)

    # 2. Gráfico de Barras - Número de Candidatos Eleitos por Partido (Comparação 2020 x 2024)
    st.subheader("Número de Candidatos Eleitos por Partido")
    eleitos_por_partido_2020 = (
        df_2020[df_2020["DS_SIT_TOT_TURNO"] == "ELEITO"]
        .groupby("SG_PARTIDO")["SQ_CANDIDATO"]
        .nunique()
    )
    eleitos_por_partido_2024 = (
        df_2024[df_2024["DS_SIT_TOT_TURNO"] == "ELEITO"]
        .groupby("SG_PARTIDO")["SQ_CANDIDATO"]
        .nunique()
    )

    partidos = list(
        set(eleitos_por_partido_2020.index).union(set(eleitos_por_partido_2024.index))
    )
    dados_partido = pd.DataFrame(
        {
            "2020": eleitos_por_partido_2020.reindex(partidos, fill_value=0),
            "2024": eleitos_por_partido_2024.reindex(partidos, fill_value=0),
        }
    )

    fig, ax = plt.subplots(figsize=(10, 6))
    dados_partido.plot(kind="bar", ax=ax)
    ax.set_ylabel("Número de Candidatos Eleitos")
    st.pyplot(fig)

    # 3. Gráfico de Barras - Distribuição de Candidatos por Município (Comparação 2020 x 2024)
    st.subheader("Distribuição de Candidatos por Município")
    candidatos_municipio_2020 = df_2020["NM_MUNICIPIO"].value_counts()
    candidatos_municipio_2024 = df_2024["NM_MUNICIPIO"].value_counts()

    municipios = list(
        set(candidatos_municipio_2020.index).union(set(candidatos_municipio_2024.index))
    )
    dados_municipio = pd.DataFrame(
        {
            "2020": candidatos_municipio_2020.reindex(municipios, fill_value=0),
            "2024": candidatos_municipio_2024.reindex(municipios, fill_value=0),
        }
    )

    fig, ax = plt.subplots(figsize=(10, 6))
    dados_municipio.plot(kind="bar", ax=ax, width=0.8)
    ax.set_ylabel("Número de Candidatos")
    ax.set_xlabel("Municípios")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
    st.pyplot(fig)

    # 4. Gráfico de Linhas - Evolução do Número de Votos Nominais por Partido (Comparação 2020 x 2024)
    st.subheader("Evolução do Número de Votos Nominais por Partido")
    votos_2020 = df_2020.groupby("SG_PARTIDO")["QT_VOTOS_NOMINAIS"].sum()
    votos_2024 = df_2024.groupby("SG_PARTIDO")["QT_VOTOS_NOMINAIS"].sum()

    partidos_votos = list(set(votos_2020.index).union(set(votos_2024.index)))
    dados_votos = pd.DataFrame(
        {
            "2020": votos_2020.reindex(partidos_votos, fill_value=0),
            "2024": votos_2024.reindex(partidos_votos, fill_value=0),
        }
    )

    fig, ax = plt.subplots(figsize=(10, 6))
    dados_votos.plot(kind="line", ax=ax, marker="o")
    ax.set_ylabel("Número de Votos Nominais")
    ax.set_xlabel("Partidos")
    st.pyplot(fig)
