from faker import Faker
from conexao import criar_conexao
import random
import mysql.connector


fake = Faker("pt_BR")

conn = criar_conexao()
cursor = conn.cursor()

def inserir_usuarios(num=35):
    for _ in range(num):
        nome = fake.name()
        senha = fake.password()
        saldo = 10000.00
        cursor.execute("INSERT INTO tbUser (Nome, Senha, Saldo) VALUES (%s, %s, %s)", (nome, senha, saldo))
    conn.commit()
    print(f"{num} usuários inseridos com sucesso!")
    
def gerar_transacoes(qtd=100):
    tipos = ['PIX', 'Transferência', 'Saque', 'Depósito']
    
    cursor.execute("SELECT Id FROM tbUser")
    ids = [row[0] for row in cursor.fetchall()]
    
    for _ in range(qtd):
        tipo = random.choice(tipos)
        quantia = random.uniform(1000.00, 10000.00)

        remetente = random.choice(ids)
        destinatario = random.choice(ids)

        # Impede que remetente e destinatário sejam iguais em transferências
        if tipo in ['PIX', 'Transferência']:
            while destinatario == remetente:
                destinatario = random.choice(ids)
        else:
            destinatario = remetente  # Saque e Depósito têm mesmo ID

        try:
            cursor.callproc('TransferirDinheiro', [remetente, destinatario, quantia, tipo])
            conn.commit()
        except mysql.connector.Error as err:
            print(f"Erro na transação: {err}")
            conn.rollback()

    print(f"{qtd} transações simuladas com sucesso!")
