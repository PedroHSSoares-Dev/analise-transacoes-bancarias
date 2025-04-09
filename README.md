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
