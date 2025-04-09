from crud import limpar_tela,pegar_id_usuario, conferir_usuario, criar_usuario, exibir_tabelas, exibir_dados_user, exibir_dados_transacoes, editar_dados, apagar_dados, exibir_saldo, depositar, saque, pix
from time import sleep

while True:
    limpar_tela()
    print("\n===== MENU =====")
    print("1. Fazer login")
    print("2. Criar usuário")
    print("3. Sair")
    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        usuario = input("Usuário: ").strip()
        senha = input("Senha: ").strip()
        
        if conferir_usuario(usuario, senha):
            print("\nLogin realizado com sucesso!")
            id_usuario = pegar_id_usuario(usuario)
            sleep(1)
            
            if usuario == "admin":  # MENU ADMINISTRADOR
                while True:
                    limpar_tela()
                    print("\n===== MENU ADMINISTRADOR =====")
                    print("1. Exibir dados")
                    print("2. Editar dados")
                    print("3. Apagar dados")
                    print("4. Voltar")
                    opcao = input("Escolha uma opção: ")
                    
                    if opcao == "1":
                        limpar_tela()
                        print("Exibindo dados...")
                        sleep(1)
                        exibir_tabelas()
                        tbEscolhida = input("Escolha a tabela que você quer visualizar: ").strip()
                        if tbEscolhida == "tbUser":
                            exibir_dados_user()
                        else:
                            exibir_dados_transacoes()
                        input("Pressione Enter para continuar...")
                        
                    elif opcao == "2":
                        limpar_tela()
                        exibir_tabelas()
                        tbEscolhida = input("Escolha a tabela que você quer editar: ").strip()
                        if tbEscolhida == "tbUser":
                            exibir_dados_user()
                        elif tbEscolhida == "tbTransacoes":
                            exibir_dados_transacoes()
                        else:
                            print("Tabela inválida.")
                            sleep(1)
                            break
                        idEscolhido = input("Digite o ID do registro que você quer editar: ").strip()
                        colunaEscolhida = input("Escolha a coluna que você quer editar: ").strip().capitalize()
                        novoValor = input("Digite o novo valor: ").strip()
                        editar_dados(tbEscolhida, colunaEscolhida, novoValor, idEscolhido)
                        if tbEscolhida == "tbUser":
                            exibir_dados_user()
                        print("Dados editados com sucesso!")
                        sleep(1)
                        input("Pressione Enter para continuar...")
                        
                    elif opcao == "3":
                        limpar_tela()
                        print("Apagando dados...")
                        sleep(1)
                        exibir_tabelas()
                        tbEscolhida = input("Escolha a tabela que você quer apagar: ").strip()
                        if tbEscolhida == "tbUser":
                            exibir_dados_user()
                        elif tbEscolhida == "tbTransacoes":
                            exibir_dados_transacoes()
                        else:
                            print("Tabela inválida.")
                            sleep(1)
                            break
                        idEscolhido = input("Digite o ID do registro que você quer apagar: ").strip()
                        apagar_dados(tbEscolhida, idEscolhido)
                        limpar_tela()
                        print("Dados apagados com sucesso!")
                        sleep(1)
                        if tbEscolhida == "tbUser":
                            exibir_dados_user()
                        else:
                            exibir_dados_transacoes()
                        input("Pressione Enter para continuar...")
                        
                    elif opcao == "4":
                        break
                        
                    else:
                        print("Opção inválida. Tente novamente.")
                        sleep(1)
            
            else:  # MENU USUÁRIO COMUM
                while True:
                    limpar_tela()
                    print("===== MENU USUÁRIO =====")
                    print("1. Depósito")
                    print("2. Saque")
                    print("3. Transferência")
                    print("4. Extrato")
                    print("5. Voltar")
                    print(f"Bem-vindo, {usuario}! {exibir_saldo(usuario)}")
                    opcao = input("Escolha uma opção: ")
                    
                    if opcao == "1":
                        limpar_tela()
                        print(exibir_saldo(usuario))
                        sleep(1)
                        valor = float(input("Digite o valor do depósito: R$"))
                        depositar(usuario, valor)
                        limpar_tela()
                        print("Depósito realizado com sucesso!")
                        sleep(1)
                        print(exibir_saldo(usuario))
                        input("Pressione Enter para continuar...")
                    
                    elif opcao == "2":
                        limpar_tela()
                        print(exibir_saldo(usuario))
                        sleep(1)
                        valor = float(input("Digite o valor do saque: R$"))
                        saque(usuario, valor)
                        limpar_tela()
                        print("Saque realizado com sucesso!")
                        sleep(1)
                        
                    elif opcao == "3":
                        limpar_tela()
                        print(exibir_saldo(usuario))
                        sleep(1)
                        valor = float(input("Digite o valor da transferência: R$"))
                        # Obter ID do destinatário pelo nome
                        destinatario_nome = input("Digite o nome do usuário de destino: ").strip()
                        destinatario_id = pegar_id_usuario(destinatario_nome)
                        
                        if destinatario_id:
                            # Passar IDs (remetente_id, destinatario_id, valor)
                            remetente_id = pegar_id_usuario(usuario)
                            pix(remetente_id, destinatario_id, valor)
                            print("Transferência realizada com sucesso!")
                        else:
                            print("Destinatário não encontrado.")
                        
                        input("Pressione Enter para continuar...")
                        
                    elif opcao == "4":
                        limpar_tela()
                        print("Exibindo extrato...")
                        sleep(1)
                        exibir_dados_transacoes(usuario)
                        input("Pressione Enter para continuar...")
                        
                    elif opcao == "5":
                        break
                        
                    else:
                        print("Opção inválida. Tente novamente.")
                        sleep(1)
                
        else:
            print("\nFalha no login. Verifique seus dados.")
            sleep(1)

    elif opcao == "2":
        novo_usuario = input("Novo usuário: ").strip()
        nova_senha = input("Nova senha: ").strip()
        
        if not novo_usuario or not nova_senha:
            print("Usuário e senha não podem estar vazios!")
            sleep(1)
            continue
            
        if criar_usuario(novo_usuario, nova_senha, 0.0):
            print("Conta criada com sucesso!")
            sleep(1)
        else:
            print("Não foi possível criar a conta.")
            sleep(1)

    elif opcao == "3":
        limpar_tela()
        print("Saindo do sistema...")
        sleep(1)
        limpar_tela()
        break

    else:
        print("Opção inválida. Digite 1, 2 ou 3.")
        sleep(1)
        limpar_tela()