from config_path import *  
import pandas as pd
from app.src.conexao import criar_conexao

def exibir_dados_transacoes():
    conn = criar_conexao()

    query = "SELECT * FROM tbTransacoes"

    dfTransacoes = pd.read_sql(query, conn)
    
    return dfTransacoes 

if __name__ == "__main__":
    print(exibir_dados_transacoes())
