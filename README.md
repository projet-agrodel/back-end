# 🌾 Agrodel - Back-End

Este é o repositório responsável pelo back-end da aplicação **Agrodel**. Utilizamos **Docker** e **Docker Compose** para facilitar a configuração e execução de todo o ambiente.

Se você está procurando o front-end da aplicação, acesse: [Agrodel Front-End](https://github.com/projet-agrodel/front-end)

---

## ✅ Requisitos

Antes de começar, certifique-se de ter o seguinte instalado em sua máquina:

* [Docker](https://www.docker.com/)

---

## Como executar o projeto

Siga os passos abaixo para iniciar o ambiente local:

1. **Clone este repositório:**

```bash
git clone https://github.com/projet-agrodel/back-end
cd back-end
```

2. **Crie um arquivo `.env` na raiz do projeto:**

Copie o conteúdo do arquivo `.env.example` e cole no novo arquivo `.env`.

```bash
cp .env.example .env
```

3. **Suba os containers com Docker Compose:**

```bash
docker-compose up -d --build
```

> O Docker irá construir e iniciar automaticamente todos os serviços necessários.

---

## 🔗 Endpoints de acesso

* **Front-End:** [http://localhost:3000](http://localhost:3000)
* **Back-End (API):** [http://localhost:5000](http://localhost:5000)
* **Banco de Dados (PostgreSQL):** acessível na porta `5432`

---

## ⚠️ Observações

* Se você já possui o **PostgreSQL** instalado localmente, pode ser necessário parar o serviço para evitar conflitos de porta com o container.
* Em alguns casos, o container do banco de dados pode demorar um pouco para estar pronto, fazendo com que o back-end falhe ao iniciar. Se isso acontecer, aguarde alguns segundos e reinicie apenas o container do back-end.
