import streamlit as st
import pandas as pd

import resumo_geral_das_eleicoes
import filtro_dinamico
import grafico_dinamico

# Configurações da barra lateral e navegação entre páginas
st.sidebar.title("Navegação")
page = st.sidebar.selectbox(
    "Escolha a página:",
    [
        "Upload de Arquivos",
        "Resumo geral das eleições",
        "Filtro dinâmico",
        "Gráficos dinâmicos",
    ],
)

# Página para upload de múltiplos arquivos CSV
if page == "Upload de Arquivos":
    st.title("Upload de Arquivos CSV")
    st.write(
        "Faça o upload de dois arquivos CSV, um para cada ano (2020 e 2024), para análise."
    )

    uploaded_files = st.file_uploader(
        "Escolha os arquivos CSV", type="csv", accept_multiple_files=True
    )

    if uploaded_files and len(uploaded_files) == 2:
        dataframes = {}

        # Ler os arquivos CSV e armazená-los em um dicionário de DataFrames (usando o nome do arquivo para identificar o ano)
        for uploaded_file in uploaded_files:
            df = pd.read_csv(uploaded_file, encoding="ISO-8859-1", sep=";")
            year = "2020" if "2020" in uploaded_file.name else "2024"
            dataframes[year] = df
            st.write(f"Visualização do arquivo para o ano **{year}**:")
            st.dataframe(df.head())  # Mostra as primeiras linhas de cada arquivo

        # Armazena os DataFrames na sessão para uso na outra página
        st.session_state["dataframes"] = dataframes
    else:
        st.write(
            "Por favor, envie exatamente dois arquivos CSV, um para cada ano (2020 e 2024)."
        )

# Página para Resumo geral das eleições
elif page == "Resumo geral das eleições":
    st.title("Resumo geral das eleições")
    if "dataframes" in st.session_state:
        resumo_geral_das_eleicoes.resumo_geral_das_eleicoes(
            st.session_state["dataframes"]
        )
    else:
        st.write(
            "Por favor, vá para a página de Upload de Arquivos e envie os arquivos CSV."
        )

elif page == "Filtro dinâmico":
    st.title("Filtro dinâmico")
    if "dataframes" in st.session_state:
        filtro_dinamico.filtro_dinamico(st.session_state["dataframes"])
    else:
        st.write(
            "Por favor, vá para a página de Upload de Arquivos e envie os arquivos CSV."
        )

elif page == "Gráficos dinâmicos":
    st.title("Gráficos dinâmicos")
    if "dataframes" in st.session_state:
        grafico_dinamico.grafico_dinamico(st.session_state["dataframes"])
    else:
        st.write(
            "Por favor, vá para a página de Upload de Arquivos e envie os arquivos CSV."
        )
