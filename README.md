### Agrodel Back-End

Este é o repositório do backend da aplicação. Utilizamos Docker para facilitar a configuração e execução.

Se você quiser executar o front-end, vá para [Agroldel Front-end](https://github.com/projet-agrodel/front-end)

## 🛠️ Requisitos

- [Docker](https://www.docker.com/) ou [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalados

## 🚀 Como rodar o backend

1. Clone este repositório:

```bash
git clone https://github.com/projet-agrodel/back-end

cd back-end
````

2. Crie um arquivo .env na raiz do projeto e copie o contéudo de .env.example e cole lá

4. Suba os containers com Docker Compose:

```bash
docker-compose up -d --build
```

> O Docker irá criar e iniciar todos os serviços necessários automaticamente.

3. Após isso o sistema estará rodando em

[http://localhost\:3000](http://localhost:3000) (Front-end)
[http://localhost\:5000](http://localhost:5000) (Back-end)
[http://localhost\:5000](http://localhost:5000) (Banco de Dados)

## Observações

1. Se tiver o postegresql na sua mquina, possa ser necessário desativar o serviço para evitar conflitos
2. Possa ser q o banco de dados demore para iniciar, fazendo com que o back-end não inicie, se isso acontecer suba o container de back-end