# Sistema Bancário - Análise de Dados

Este projeto complementa o [CRUD bancário em Python](https://github.com/PedroHSSoares-Dev/crud) com foco em **Engenharia de Dados**, **Ciência de Dados** e **Visualização**.

---

## 🔍 Objetivo

Realizar um pipeline de análise de dados com base nas transações bancárias registradas pelo sistema:

- 📥 Extração de dados do banco MySQL
- 🧹 Transformação e limpeza com Pandas
- 📊 Visualização com Matplotlib/Seaborn
- 📈 (Opcional) Dashboard com Streamlit ou Power BI

---

## 📁 Estrutura do Projeto

```
sistema_bancario/
├── analise/
│   ├── extrair_dados.py     # Conecta e extrai dados do MySQL
│   ├── transformar_dados.py # Limpa e transforma os dados
│   ├── graficos.py          # Gera visualizações
│   └── dashboard.py         # (Opcional) Dashboard com Streamlit
├── app/                     # Projeto CRUD original (cópia ou submódulo)
├── relatorio_transacoes.csv # Exportação para Power BI
├── requirements.txt         # Dependências
└── README.txt               # Este arquivo
```

---

## ⚙️ Tecnologias

- Python
- Pandas
- Matplotlib / Seaborn
- MySQL
- Docker 
- Streamlit 
- Power BI 

---

## 🚀 Como executar

1. Clone este repositório:

```bash
git clone https://github.com/SeuUsuario/sistema-bancario-analise-dados
cd sistema-bancario-analise-dados
```

2. Instale os pacotes:

```bash
pip install -r requirements.txt
```

3. Execute os scripts de análise:

```bash
python analise/extrair_dados.py
python analise/transformar_dados.py
python analise/graficos.py
```

4. (Opcional) Rode o dashboard:

```bash
streamlit run analise/dashboard.py
```

---

## 📊 Exemplos de análise

- Total movimentado por usuário
- Volume de transações por mês
- Gráfico de distribuição por tipo de operação (PIX, saque, depósito)

---

## 🤝 Créditos

Projeto base: [CRUD bancário em Python](https://github.com/PedroHSSoares-Dev/crud)  
Autor: Pedro Henrique Soares  


