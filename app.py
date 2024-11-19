import streamlit as st
import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt

# Configuração do banco de dados
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "rootpassword",
    "database": "codespaces_db"
}

# Função para conectar ao banco de dados e carregar dados
def load_data():
    try:
        connection = mysql.connector.connect(**db_config)
        query = "SELECT * FROM student_scores"
        df = pd.read_sql(query, connection)
        connection.close()
        return df
    except Exception as e:
        st.error(f"Erro ao conectar ao banco de dados: {e}")
        return pd.DataFrame()

# Inicialização do app
st.title("Análise da Tabela Student Scores")
st.write("Este aplicativo gera gráficos a partir da tabela `student_scores`.")

# Carregar os dados
data = load_data()

if data.empty:
    st.warning("Nenhum dado encontrado na tabela.")
else:
    st.dataframe(data)  # Exibe a tabela

    # Gráfico 1: Distribuição das médias (average_score)
    st.subheader("Distribuição das Médias")
    plt.figure()
    plt.hist(data["average_score"], bins=10, edgecolor="black", alpha=0.7)
    plt.title("Distribuição das Médias")
    plt.xlabel("Média")
    plt.ylabel("Frequência")
    st.pyplot(plt)

    # Gráfico 2: Média das pontuações por grupo étnico
    st.subheader("Média das Pontuações por Grupo Étnico")
    group_means = data.groupby("race_ethnicity")[["math_score", "reading_score", "writing_score"]].mean()
    group_means.plot(kind="bar", figsize=(8, 5))
    plt.title("Média das Pontuações por Grupo Étnico")
    plt.xlabel("Grupo Étnico")
    plt.ylabel("Pontuação Média")
    st.pyplot(plt)

    # Gráfico 3: Distribuição de pontuações por gênero
    st.subheader("Distribuição de Pontuações por Gênero")
    plt.figure()
    genders = data.groupby("gender")[["math_score", "reading_score", "writing_score"]].mean()
    genders.plot(kind="bar", figsize=(8, 5))
    plt.title("Distribuição de Pontuações por Gênero")
    plt.xlabel("Gênero")
    plt.ylabel("Pontuação Média")
    st.pyplot(plt)
