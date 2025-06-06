# 🐳 Projeto Agrodrel

Este projeto é composto por dois repositórios separados:

- **Frontend** (`front`)
- **Backend** (`back`)

---
## 📁 Estrutura de Diretórios

A estrutura esperada após clonar e organizar os repositórios é a seguinte:

```
agrodrel/
├── back-end/
├── front-end/
└── docker-compose.yml
```

---

## 🚀 Passo a Passo

### 1. Clone os Repositórios

Crie uma pasta principal para o projeto e entre nela:

```bash
mkdir agrodrel
cd agrodrel
```

Clone os dois repositórios dentro dessa pasta:

```bash
git clone https://github.com/projet-agrodel/front-end front-end
git clone https://github.com/projet-agrodel/back-end back-end
```

> 📝 Substitua os links acima pelos repositórios reais.

---

### 2. Mova o `docker-compose.yml` que está na pasta end para a raiz

O arquivo `docker-compose.yml` estiver dentro da pasta `front/`, mova-o para a raiz da pasta principal:

```bash
mv front/docker-compose.yml .
```

---

### 3. Inicie os Containers

Com tudo organizado, execute o seguinte comando na raiz do projeto:

```bash
docker-compose up --build
```

Esse comando irá:

- Construir as imagens do frontend e backend e banco de dados
- Subir os containers
- Expor as portas configuradas no `docker-compose.yml`

---

## ✅ Acesso aos Serviços

- Frontend: [http://localhost:3000](http://localhost:3000)
- Backend: [http://localhost:5000](http://localhost:5000)
- Banco de Dados: [http://localhost:5432](http://localhost:5432)

## 🛠️ Observações

- Verifique se as portas 3000 (frontend) e 5000 e 5432 (backend) estão livres no seu sistema.
- Se necessário, edite o `docker-compose.yml` para ajustar caminhos de build e nomes de serviços.
- Se tiver o Postgres instalado na sua máquina, desative seu serviço caso o container do banco de dados não subir.