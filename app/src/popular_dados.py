from faker import Faker
from conexao import criar_conexao
import random
import mysql.connector
from datetime import datetime, timedelta


fake = Faker("pt_BR")

conn = criar_conexao()
cursor = conn.cursor()

def inserir_usuarios(num=5000):
    for _ in range(num):
        nome = fake.name()
        senha = fake.password()
        saldo = random.uniform(1000.00, 10000.00)
        cursor.execute("INSERT INTO tbUser (Nome, Senha, Saldo) VALUES (%s, %s, %s)", (nome, senha, saldo))
    conn.commit()
    print(f"{num} usuários inseridos com sucesso!")
    
def gerar_data_aleatoria():
    inicio = datetime(2025, 1, 1)
    hoje = datetime.now()
    dias_total = (hoje - inicio).days
    data_aleatoria = inicio + timedelta(days=random.randint(0, dias_total),
                                        seconds=random.randint(0, 86400))
    return data_aleatoria.strftime('%Y-%m-%d %H:%M:%S')

    
def gerar_transacoes(qtd=10000):
    tipos = ['PIX', 'Transferência', 'Saque', 'Depósito']
    
    cursor.execute("SELECT Id FROM tbUser")
    ids = [row[0] for row in cursor.fetchall()]
    
    for _ in range(qtd):
        tipo = random.choice(tipos)
        quantia = round(random.uniform(10.00, 10000.00), 2)

        remetente = random.choice(ids)
        destinatario = random.choice(ids)

        if tipo in ['PIX', 'Transferência']:
            while destinatario == remetente:
                destinatario = random.choice(ids)
        else:
            destinatario = remetente

        datahora = gerar_data_aleatoria()

        try:
            cursor.execute("""
                INSERT INTO tbTransacoes (RemetenteId, DestinatarioId, Quantia, DataHora, Tipo)
                VALUES (%s, %s, %s, %s, %s)
            """, (remetente, destinatario, quantia, datahora, tipo))

            conn.commit()
        except mysql.connector.Error as err:
            print(f"Erro ao inserir transação: {err}")
            conn.rollback()

    print(f"{qtd} transações simuladas com sucesso!")

if __name__ == "__main__":
    inserir_usuarios()
    gerar_transacoes()
