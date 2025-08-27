
Este repositório contém o projeto prático desenvolvido para a disciplina de **Programação WEB I**. A aplicação consiste em uma agenda de contatos simples, onde é possível realizar as quatro operações básicas de um banco de dados (CRUD: Create, Read, Update, Delete) através de uma interface web.

## 🚀 Sobre o Projeto

O objetivo principal desta atividade é demonstrar a integração entre uma aplicação web backend, desenvolvida com o framework Flask em Python, e um banco de dados relacional PostgreSQL. A aplicação permite gerenciar uma lista de usuários, com funcionalidades de cadastro, listagem, edição e exclusão.

### ✨ Funcionalidades

* **Cadastro de usuários:** Criação de novos registros no banco de dados.
* **Listagem de usuários:** Visualização de todos os usuários cadastrados em uma tabela.
* **Edição de usuários:** Atualização das informações de um usuário existente.
* **Exclusão de usuários:** Remoção de um registro do banco de dados.
* **Segurança:** As senhas são armazenadas de forma segura utilizando hash bcrypt.

## 🛠️ Tecnologias Utilizadas

Este projeto foi construído utilizando as seguintes tecnologias:

* **Backend:** Python 3, Flask
* **Banco de Dados:** PostgreSQL
* **Frontend:** HTML5, Jinja2 (template engine do Flask)
* **Bibliotecas Python:**
    * `psycopg[binary,pool]` para a conexão com o PostgreSQL.
    * `bcrypt` para hashing de senhas.
    * `python-dotenv` para gerenciar variáveis de ambiente.

## ⚙️ Pré-requisitos

Antes de começar, você vai precisar ter instalado em sua máquina:
* [Python 3](https://www.python.org/)
* [PostgreSQL](https://www.postgresql.org/download/)
* [Git](https://git-scm.com/)

## 🏁 Como Executar o Projeto

Siga os passos abaixo para executar a aplicação localmente:

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/SAUL-ALVES/atv-flask-postgres.git
    cd SEU-REPOSITORIO
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    python -m venv venv
    # No Windows
    venv\Scripts\activate
    # No Linux/Mac
    source venv/bin/activate
    ```

3.  **Instale as dependências do projeto:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Observação: Se você ainda não tem um arquivo `requirements.txt`, gere-o com o comando `pip freeze > requirements.txt`)*

4.  **Configure o Banco de Dados:**
    * Certifique-se de que seu servidor PostgreSQL está rodando.
    * Crie o banco de dados e execute os scripts de estrutura e dados iniciais:
    ```bash
    # Conecte-se ao psql
    psql -U postgres

    # Crie o banco de dados
    CREATE DATABASE web1;

    # Saia do psql (\q) e execute os scripts a partir do terminal comum
    psql -U postgres -d web1 -f schema.sql
    psql -U postgres -d web1 -f seed.sql
    ```

5.  **Configure as Variáveis de Ambiente:**
    * Crie uma cópia do arquivo de exemplo `.env.example` (se houver) ou crie um novo arquivo chamado `.env` na raiz do projeto.
    * Adicione a sua string de conexão com o banco de dados:
    ```
    DATABASE_URL=postgresql://postgres:SUA_SENHA@localhost:5432/web1
    ```

6.  **Execute a aplicação:**
    ```bash
    flask run
    ```

7.  Abra seu navegador e acesse `http://127.0.0.1:5000` ou `http://localhost:5000`.

## 👨‍💻 Saul Alves

