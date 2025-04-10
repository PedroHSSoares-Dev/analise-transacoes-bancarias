# 💳 Análise de Transações Bancárias com Python

Este projeto combina um sistema bancário CRUD em Python com uma estrutura de análise de dados para explorar e visualizar transações registradas no banco de dados.

---

## 📦 Estrutura do Projeto

```
analise-transacoes-bancarias/
├── analise/                   ← scripts para análise de dados
│   ├── extrair_dados.py       ← extrai dados do MySQL para Pandas
│   ├── transformar_dados.py   ← limpa e transforma os dados
│   ├── graficos.py            ← gera gráficos com matplotlib/seaborn
│   └── dashboard.py           ← dashboard interativo com Streamlit
├── app/                       ← aplicação CRUD em Python
│   ├── docker/
│   │   ├── docker-compose.yml ← banco de dados MySQL com Docker
│   │   └── init.sql           ← script de criação da base
│   └── src/
│       ├── conexao.py         ← conexão com banco de dados
│       ├── crud.py            ← funções de operações (inserir, sacar, etc)
│       └── menu.py            ← interface terminal com menu interativo
└── README.md                  ← este arquivo
```

---

## 🎯 Objetivo

Unir a prática de desenvolvimento com Python + MySQL com fundamentos de:

- 🧪 Engenharia de Dados
- 📊 Análise de Dados
- 📈 Visualização de Dados
- 🧠 Ciência de Dados

---

## ⚙️ Pré-requisitos

- **Python**: Versão 3.8 ou superior (recomendado 3.9)
- **Docker**: Versão 20.10 ou superior
- **Docker Compose**: Versão 1.29 ou superior
- **Bibliotecas Python**: Instale as bibliotecas listadas no `requirements.txt`

---

## 🛠️ Instalação

1. **Instale o Python**:
   - Baixe a versão mais recente do [Python](https://www.python.org/downloads/) (versão 3.8 ou superior).
   - Durante a instalação, marque a opção "Add Python to PATH".
2. **Instale o Docker**:
   - Siga as instruções de instalação do [Docker Desktop](https://www.docker.com/products/docker-desktop/) para o seu sistema operacional.
   - Certifique-se de que o Docker esteja em execução após a instalação.
3. **Instale as dependências Python**:
   - Navegue até o diretório do projeto no terminal.
   - Execute o seguinte comando para instalar as bibliotecas necessárias:
     ```bash
     pip install -r requirements.txt
     ```

--

## 🚀 Como executar

### 1. Suba o banco de dados com Docker:

```bash
cd app/docker
docker-compose up -d
```

### 2. Rode o sistema bancário via terminal:

```bash
cd ../src
python menu.py
```

### 3. Execute os scripts de análise:

```bash
cd ../../analise
python extrair_dados.py
python transformar_dados.py
python graficos.py
```

### 4. Rode o dashboard (opcional):

```bash
streamlit run dashboard.py
```
---

## 💻 Uso

1. **Inicie o sistema**:
   - No diretório do projeto, execute o seguinte comando para iniciar o sistema usando Docker Compose:
     ```bash
     docker-compose up --build
     ```
2. **Acesse a interface web**:
   - Abra seu navegador e acesse `http://localhost:8501` para visualizar a interface do Streamlit.
3. **Fluxo de trabalho típico**:
   - **Login**: Insira suas credenciais na página de login.
   - **Registro de transação**: Navegue até a seção de "Transações" e preencha os detalhes da transação (valor, descrição, categoria).
   - **Geração de relatório**: Vá para a seção de "Relatórios" e selecione o período desejado para gerar um relatório financeiro.

---

## 📊 Tipos de análise realizadas

- Total movimentado por usuário
- Volume de transações por mês
- Distribuição de transações (saque, depósito, pix)
- Dashboard interativo com filtros

---

## 🛠 Tecnologias usadas

- Python (CRUD + análise)
- MySQL (base de dados)
- Pandas, Matplotlib, Seaborn
- Streamlit (dashboard web)
- Docker (banco em container)

---

## 👨‍💻 Autor

Desenvolvido por Pedro Henrique Soares  
Repositório original do CRUD: https://github.com/PedroHSSoares-Dev/crud  
Análise de dados adaptada com auxílio do ChatGPT
