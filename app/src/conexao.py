from dotenv import load_dotenv
import mysql.connector
import os

# Carrega as variáveis do .env
load_dotenv()

def criar_conexao():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            port=int(os.getenv("DB_PORT")),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            charset="utf8mb4",
            collation='utf8mb4_unicode_ci',
            use_unicode=True
        )
        return conn
    except mysql.connector.Error as err:
        print("Erro de conexão:", err)
        return None
