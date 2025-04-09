from conexao import criar_conexao
from tabulate import tabulate
import mysql.connector
import os


def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def pegar_id_usuario(usuario):
    conn = criar_conexao()
    if conn is None:
        return None
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT Id FROM tbUser WHERE Nome = %s", (usuario,))
        resultado = cursor.fetchone()
        return resultado[0] if resultado else None
    except mysql.connector.Error as err:
        print("Erro ao pegar ID do usuário:", err)
        return None
    finally:
        cursor.close()
        conn.close()

def conferir_usuario(user, senha):
    conn = criar_conexao()
    if conn is None:
        return False
    
    cursor = conn.cursor()
    try:
        # Verifica usuário e senha juntos
        cursor.execute(
            "SELECT * FROM tbUser WHERE Nome = %s AND Senha = %s",  # Correção aqui
            (user, senha)  # Faltava o parêntese de fechamento
        )
        resultado = cursor.fetchone()
        return resultado is not None
    except mysql.connector.Error as err:
        print("Erro ao verificar usuário:", err)
        return False
    finally:
        cursor.close()
        conn.close()

def criar_usuario(user, senha, saldo):
    conn = criar_conexao()
    if conn is None:
        return False

    cursor = conn.cursor()
    try:
        # Verifica se usuário já existe
        cursor.execute("SELECT * FROM tbUser WHERE Nome = %s", (user,))
        if cursor.fetchone():
            print("Usuário já existe!")
            return False

        # Cria novo usuário
        cursor.execute(
            "INSERT INTO tbUser (Nome, Senha, Saldo) VALUES (%s, %s, %s)",
            (user, senha, saldo)
        )
        conn.commit()  # Importante para salvar no banco
        print("Usuário criado com sucesso!")
        return True
    except mysql.connector.Error as err:
        print("Erro ao criar usuário:", err)
        return False
    finally:
        cursor.close()
        conn.close()
        
def exibir_tabelas():
    conn = criar_conexao()
    if conn is None:
        return

    cursor = conn.cursor()
    try:
        cursor.execute("SHOW TABLES")
        tabelas = cursor.fetchall()
        print("Tabelas no banco de dados:")
        for tabela in tabelas:
            print(tabela[0])
    except mysql.connector.Error as err:
        print("Erro ao exibir tabelas:", err)
    finally:
        cursor.close()
        conn.close()

def exibir_dados_transacoes(user="admin"):
    conexao = None
    cursor = None
    try:
        conexao = criar_conexao()
        cursor = conexao.cursor()
        
        # Se o usuário não for admin, busque o ID correspondente ao nome
        if user != "admin":
            cursor.execute("SELECT Id FROM tbUser WHERE Nome = %s", (user,))
            row = cursor.fetchone()
            if row:
                user_id = row[0]
            else:
                print("Usuário não encontrado.")
                return
            # Filtra as transações do usuário (RemetenteId = user_id)
            cursor.execute("SELECT * FROM tbTransacoes WHERE RemetenteId = %s", (user_id,))
        else:
            # Se for admin, exibe todas as transações
            cursor.execute("SELECT * FROM tbTransacoes")
            
        resultado = cursor.fetchall()
        
        dados_formatados = []
        for linha in resultado:
            quantia = float(linha[3])  # Quantia está na coluna de índice 3
            dados_formatados.append([
                linha[0],  # Id da Transação
                linha[1],  # RemetenteId
                f"R$ {quantia:,.2f}".replace(".", "X").replace(",", ".").replace("X", ","),  # Formatação BR
                linha[2],  # DestinatarioId
                linha[4]   # Data e Hora
            ])
            
        print(tabulate(
            dados_formatados,
            headers=["ID", "RemetenteId", "Quantia", "DestinatarioId", "Data e Hora"],
            tablefmt="pretty",
            numalign="right"
        ))
        print(f'{len(dados_formatados)} registros encontrados.')
    
    except mysql.connector.Error as e:
        print(f"Erro de banco de dados: {e}")
    finally:
        if cursor:
            cursor.close()
        if conexao and conexao.is_connected():
            conexao.close()

           
def exibir_dados_user():
    conexao = None
    cursor = None
    try:
        # Cria conexão usando sua função (supondo que criar_conexao() retorna uma conexão válida)
        conexao = criar_conexao()
        cursor = conexao.cursor()
        
        cursor.execute("SELECT * FROM tbUser")
        resultado = cursor.fetchall()
        
        dados_formatados = []
        for linha in resultado:
            saldo = float(linha[3])  # Conversão para float
            dados_formatados.append([
                linha[0],  # ID
                linha[1],  # Usuário
                "******",  # Mascarando senha (boas práticas)
                f"R$ {saldo:,.2f}".replace(".", "X").replace(",", ".").replace("X", ",")  # Formatação BR
            ])
            
        print(tabulate(
            dados_formatados,
            headers=["ID", "Nome", "Senha", "Saldo"],
            tablefmt="pretty",
            numalign="right"
        ))
        print(f'{len(dados_formatados)} registros encontrados.')
        
    
    except mysql.connector.Error as e:
        print(f"Erro de banco de dados: {e}")
    finally:
        # Fechar recursos corretamente
        if cursor:
            cursor.close()
        if conexao and conexao.is_connected():
            conexao.close()
            
def editar_dados(tabela, coluna, novo_valor, condicao):
    conn = criar_conexao()
    if conn is None:
        return
    
    cursor = conn.cursor()
    try:
        query = f"UPDATE {tabela} SET {coluna} = %s WHERE id = {condicao}"
        cursor.execute(query, (novo_valor,))
        conn.commit()  # Importante para salvar no banco
        print("Dados atualizados com sucesso!")
    except mysql.connector.Error as err:
        print("Erro ao atualizar dados:", err)
    finally:
        cursor.close()
        conn.close()

def apagar_dados(tabela, condicao):
    conn = criar_conexao()
    if conn is None:
        return
    
    cursor = conn.cursor()
    try:
        query = f"DELETE FROM {tabela} WHERE id = {condicao}"
        cursor.execute(query)
        conn.commit()  # Importante para salvar no banco
        print("Dados apagados com sucesso!")
    except mysql.connector.Error as err:
        print("Erro ao apagar dados:", err)
    finally:
        cursor.close()
        conn.close()
        
def exibir_saldo(usuario):
    conn = criar_conexao()
    if conn is None:
        return "Erro ao conectar ao banco de dados."

    cursor = conn.cursor()
    try:
        cursor.execute("SELECT Saldo FROM tbUser WHERE Nome = %s", (usuario,))
        resultado = cursor.fetchone()
        if resultado:
            saldo = resultado[0]
            return f"Seu saldo atual é: R$ {saldo:.2f}"
        else:
            return "Usuário não encontrado."
    except mysql.connector.Error as err:
        return f"Erro ao exibir saldo: {err}"
    finally:
        cursor.close()
        conn.close()

        
def depositar(usuario, valor):
    conn = criar_conexao()
    if conn is None:
        return
    cursor = conn.cursor()
    try:
        # Verifica se o valor é positivo
        if valor <= 0:
            print("Valor inválido para depósito.")
            return
        
        # Atualiza o saldo do usuário
        cursor.execute("UPDATE tbUser SET Saldo = Saldo + %s WHERE Nome = %s", (valor, usuario))
        conn.commit() 
        print(f"Depósito de R$ {valor:.2f} realizado com sucesso!")
    except mysql.connector.Error as err:
        print("Erro ao depositar:", err)
    finally:
        cursor.close()
        conn.close()
        
def saque(usuario, valor):
    conn = criar_conexao()
    if conn is None:
        return
    cursor = conn.cursor()
    try:
        # Verifica se o valor é suficiente
        cursor.execute("SELECT Saldo FROM tbUser WHERE Nome = %s", (usuario,))
        resultado = cursor.fetchone()
        if resultado:
            saldo = resultado[0]
            if valor > saldo:
                print("Saldo insuficiente para saque.")
                return
        else:
            print("Usuário não encontrado.")
            return
        
        # Atualiza o saldo do usuário
        cursor.execute("UPDATE tbUser SET Saldo = Saldo - %s WHERE Nome = %s", (valor, usuario))
        conn.commit() 
        print(f"Saque de R$ {valor:.2f} realizado com sucesso!")
    except mysql.connector.Error as err:
        print("Erro ao sacar:", err)
    finally:
        cursor.close()
        conn.close()
        
def pix(remetente_id, destinatario_id, valor):
    conn = criar_conexao()
    if conn is None:
        print("Erro: Não foi possível conectar ao banco de dados.")
        return
    cursor = conn.cursor()
    
    try:
        # Chama a procedure usando IDs (inteiros)
        cursor.callproc('TransferirDinheiro', (remetente_id, destinatario_id, valor))
        conn.commit()
        print(f"Transferência de R$ {valor:.2f} realizada com sucesso!")
    
    except mysql.connector.Error as err:
        print(f"Erro ao realizar a transferência: {err}")
    
    finally:
        cursor.close()
        conn.close()
