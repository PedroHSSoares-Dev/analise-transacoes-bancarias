from conexao import criar_conexao
from tabulate import tabulate
import mysql.connector
import os
from datetime import datetime  # Adicionado pra pegar a data/hora atual

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
        cursor.execute("SELECT * FROM tbUser WHERE Nome = %s AND Senha = %s", (user, senha))
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
        cursor.execute("SELECT * FROM tbUser WHERE Nome = %s", (user,))
        if cursor.fetchone():
            print("Usuário já existe!")
            return False
        cursor.execute("INSERT INTO tbUser (Nome, Senha, Saldo) VALUES (%s, %s, %s)", (user, senha, saldo))
        conn.commit()
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
        
        if user != "admin":
            cursor.execute("SELECT Id FROM tbUser WHERE Nome = %s", (user,))
            row = cursor.fetchone()
            if row:
                user_id = row[0]
            else:
                print("Usuário não encontrado.")
                return
            cursor.execute("SELECT * FROM tbTransacoes WHERE RemetenteId = %s", (user_id,))
        else:
            cursor.execute("SELECT * FROM tbTransacoes")
            
        resultado = cursor.fetchall()
        
        dados_formatados = []
        for linha in resultado:
            quantia = float(linha[3])
            dados_formatados.append([
                linha[0],  # Id da Transação
                linha[1],  # RemetenteId
                linha[2],  # DestinatarioId (pode ser NULL)
                f"R$ {quantia:,.2f}".replace(".", "X").replace(",", ".").replace("X", ","),  # Formatação BR
                linha[4],  # DataHora
                linha[5]   # Tipo (novo campo)
            ])
            
        print(tabulate(
            dados_formatados,
            headers=["ID", "RemetenteId", "DestinatarioId", "Quantia", "Data e Hora", "Tipo"],
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
        conexao = criar_conexao()
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM tbUser")
        resultado = cursor.fetchall()
        
        dados_formatados = []
        for linha in resultado:
            saldo = float(linha[3])
            dados_formatados.append([
                linha[0],
                linha[1],
                "******",
                f"R$ {saldo:,.2f}".replace(".", "X").replace(",", ".").replace("X", ",")
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
        query = f"UPDATE {tabela} SET {coluna} = %s WHERE id = %s"  # Corrigido pra usar placeholder
        cursor.execute(query, (novo_valor, condicao))
        conn.commit()
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
        query = f"DELETE FROM {tabela} WHERE id = %s"  # Corrigido pra usar placeholder
        cursor.execute(query, (condicao,))
        conn.commit()
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
        if valor <= 0:
            print("Valor inválido para depósito.")
            return
        user_id = pegar_id_usuario(usuario)
        if not user_id:
            print("Usuário não encontrado.")
            return
        # Usa a procedure pra registrar o depósito
        data_atual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.callproc('TransferirDinheiro', (user_id, None, valor, data_atual, 'Depósito'))
        conn.commit()
        print(f"Depósito de R$ {valor:.2f} realizado com sucesso!")
    except mysql.connector.Error as err:
        print(f"Erro ao depositar: {err}")
    finally:
        cursor.close()
        conn.close()

def saque(usuario, valor):
    conn = criar_conexao()
    if conn is None:
        return
    cursor = conn.cursor()
    try:
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
        user_id = pegar_id_usuario(usuario)
        # Usa a procedure pra registrar o saque
        data_atual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.callproc('TransferirDinheiro', (user_id, None, valor, data_atual, 'Saque'))
        conn.commit()
        print(f"Saque de R$ {valor:.2f} realizado com sucesso!")
    except mysql.connector.Error as err:
        print(f"Erro ao sacar: {err}")
    finally:
        cursor.close()
        conn.close()

def pix(remetente_id, destinatario_id, valor, tipo='Transferência'):
    conn = criar_conexao()
    if conn is None:
        print("Erro: Não foi possível conectar ao banco de dados.")
        return
    cursor = conn.cursor()
    try:
        # Adiciona data atual e tipo
        data_atual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.callproc('TransferirDinheiro', (remetente_id, destinatario_id, valor, data_atual, tipo))
        conn.commit()
        print(f"Transferência de R$ {valor:.2f} ({tipo}) realizada com sucesso!")
    except mysql.connector.Error as err:
        print(f"Erro ao realizar a transferência: {err}")
    finally:
        cursor.close()
        conn.close()