import mysql.connector

def criar_conexao():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password="123456",
            database="meu_banco"
        )
        return conn
    except mysql.connector.Error as err:
        print("Erro de conexão:", err)
        return None