# 🏦 Análise de Transações Bancárias com Python

Este projeto combina um sistema bancário CRUD em Python com uma estrutura de análise de dados para explorar e visualizar transações registradas no banco de dados.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Pandas](https://img.shields.io/badge/Pandas-1.3+-green.svg)
![MySQL](https://img.shields.io/badge/MySQL-8.0+-orange.svg)
![Docker](https://img.shields.io/badge/Docker-20.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.10+-red.svg)

## 📋 Índice

- [Visão Geral](#visão-geral)
- [Funcionalidades](#funcionalidades)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Requisitos](#requisitos)
- [Instalação](#instalação)
- [Uso](#uso)
  - [Aplicação CRUD](#aplicação-crud)
  - [Análise de Dados](#análise-de-dados)
  - [Dashboard](#dashboard)
- [Exemplos](#exemplos)
- [Contribuição](#contribuição)
- [Licença](#licença)

## 🔍 Visão Geral

Este projeto foi desenvolvido para demonstrar a integração entre um sistema bancário simples e ferramentas de análise de dados. A aplicação permite:

1. Gerenciar contas bancárias e transações através de uma interface de terminal
2. Armazenar dados em um banco MySQL (configurado via Docker)
3. Extrair e transformar dados para análise com Pandas
4. Visualizar padrões e insights através de gráficos e dashboards interativos

## ✨ Funcionalidades

### Sistema Bancário (CRUD)
- Criar e gerenciar contas de usuários
- Registrar depósitos, saques e transferências
- Consultar saldo e histórico de transações
- Armazenar dados em banco MySQL

### Análise de Dados
- Extração de dados do MySQL para DataFrames Pandas
- Limpeza e transformação de dados
- Análise estatística de transações
- Visualização de dados com Matplotlib/Seaborn
- Dashboard interativo com Streamlit

## 📁 Estrutura do Projeto

```
analise-transacoes-bancarias/
├── analise/                      ← scripts para análise de dados
│   ├── extrair_dados.py          ← extrai dados do MySQL para Pandas
│   ├── transformar_dados.py      ← limpa e transforma os dados
│   ├── graficos.ipynb            ← gera gráficos com matplotlib/seaborn
│   ├── config_path.py            ← configurações de caminhos
│   └── dashboard.py              ← dashboard interativo com Streamlit
├── app/                          ← aplicação CRUD em Python
│   ├── docker/                   ← configuração do ambiente Docker
│   │   ├── docker-compose.yml    ← banco de dados MySQL com Docker
│   │   └── init.sql              ← script de criação da base
│   └── src/                      ← código-fonte da aplicação
│       ├── conexao.py            ← conexão com banco de dados
│       ├── crud.py               ← funções de operações (inserir, sacar, etc)
│       └── menu.py               ← interface terminal com menu interativo
├── .gitignore                    ← arquivos ignorados pelo git
├── README.md                     ← este arquivo
└── requirements.txt              ← dependências do projeto
```

## 📋 Requisitos

- Python 3.8+
- Docker e Docker Compose
- MySQL 8.0+
- Bibliotecas Python (ver `requirements.txt`)

## 🚀 Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/PedroHSSoares-Dev/analise-transacoes-bancarias.git
   cd analise-transacoes-bancarias
   ```

2. Crie e ative um ambiente virtual (recomendado):
   ```bash
   python -m venv venv
   # No Windows
   venv\Scripts\activate
   # No Linux/Mac
   source venv/bin/activate
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Inicie o banco de dados MySQL com Docker:
   ```bash
   cd app/docker
   docker-compose up -d
   ```

## 🖥️ Uso

### Aplicação CRUD

Para iniciar a aplicação bancária:

```bash
cd app/src
python menu.py
```

Siga as instruções no terminal para:
- Criar uma nova conta
- Realizar depósitos e saques
- Transferir valores entre contas
- Consultar saldo e histórico de transações

### Análise de Dados

Para extrair e transformar dados para análise:

```bash
cd analise
python extrair_dados.py
python transformar_dados.py
```

Para gerar visualizações, você pode executar o notebook Jupyter:

```bash
jupyter notebook analise/graficos.ipynb
```

### Dashboard

Para iniciar o dashboard interativo:

```bash
cd analise
streamlit run dashboard.py
```

Acesse o dashboard em seu navegador através do endereço: `http://localhost:8501`

## 📊 Exemplos

### Exemplo de Análise de Transações

O projeto permite analisar padrões de transações como:
- Volume de transações por período
- Tipos de transações mais comuns
- Valores médios de transações
- Identificação de outliers e transações suspeitas

### Exemplo de Visualização

O dashboard interativo permite filtrar e visualizar dados de diferentes formas:
- Gráficos de linha para tendências temporais
- Gráficos de barra para comparação de categorias
- Mapas de calor para correlações
- Tabelas interativas para exploração detalhada

## 🤝 Contribuição

Contribuições são bem-vindas! Para contribuir:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Faça commit das suas alterações (`git commit -m 'Adiciona nova funcionalidade'`)
4. Faça push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para detalhes.

---

Desenvolvido por [PedroHSSoares-Dev](https://github.com/PedroHSSoares-Dev)
