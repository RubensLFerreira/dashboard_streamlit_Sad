import streamlit as st
import pandas as pd


def resumo_geral_das_eleicoes(dataframes):
    for year, df in dataframes.items():
        st.subheader(f"Resumo Geral das Eleições de {year}")

        # 1. Número total de candidatos inscritos
        total_candidatos = df["SQ_CANDIDATO"].nunique()

        # 2. Número de candidatos eleitos
        candidatos_eleitos = df[df["DS_SIT_TOT_TURNO"] == "ELEITO"][
            "SQ_CANDIDATO"
        ].nunique()

        # 3. Número de municípios distintos
        total_municipios = df["NM_MUNICIPIO"].nunique()

        # 4. Número de candidatos eleitos por partido
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

        # Exibir a tabela de resumo no Streamlit para o ano específico
        st.table(tabela_resultados)

        # Exibir candidatos eleitos por partido
        st.write(f"Número de Candidatos Eleitos por Partido em {year}")
        st.table(eleitos_por_partido)
