import csv
import mysql.connector
from mysql.connector import Error

# Configuração do banco de dados
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "rootpassword",
    "database": "codespaces_db"
}

# Nome do arquivo CSV
csv_file = "Cleaned_Students_Performance.csv"

# Função para criar conexão com o banco de dados
def create_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            print("Conexão com o MySQL bem-sucedida")
        return connection
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        return None

# Função para criar a tabela se não existir
def create_table(connection):
    create_table_query = """
    CREATE TABLE IF NOT EXISTS student_scores (
        gender INT,
        race_ethnicity VARCHAR(50),
        parental_level_of_education VARCHAR(50),
        lunch INT,
        test_preparation_course INT,
        math_score INT,
        reading_score INT,
        writing_score INT,
        total_score INT,
        average_score FLOAT
    );
    """
    cursor = connection.cursor()
    cursor.execute(create_table_query)
    connection.commit()
    print("Tabela criada/verificada com sucesso")

# Função para inserir dados no banco de dados
def insert_data_from_csv(connection, csv_file):
    insert_query = """
    INSERT INTO student_scores (
        gender, race_ethnicity, parental_level_of_education, lunch, test_preparation_course,
        math_score, reading_score, writing_score, total_score, average_score
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """
    cursor = connection.cursor()
    with open(csv_file, "r") as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Pular o cabeçalho
        for row in csv_reader:
            cursor.execute(insert_query, row)
    connection.commit()
    print("Dados inseridos com sucesso")

# Função principal
def main():
    connection = create_connection()
    if connection:
        create_table(connection)
        insert_data_from_csv(connection, csv_file)
        connection.close()
        print("Conexão encerrada")

if __name__ == "__main__":
    main()
