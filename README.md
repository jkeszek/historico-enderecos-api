# API de Histórico de Endereços

API REST desenvolvida em Python com FastAPI para armazenamento e gerenciamento do histórico de endereços consultados pela API principal do projeto.

A aplicação permite cadastrar, consultar, atualizar e excluir endereços armazenados em um banco de dados SQLite.

---

## Sobre o projeto

Esta API funciona como componente secundário da aplicação de consulta de CEP.

A API principal consulta os dados de um CEP através do ViaCEP e envia o endereço obtido para esta API, que é responsável por registrar e manter o histórico das consultas.

**Porta:** `8001`

A documentação das rotas é disponibilizada automaticamente através do Swagger/OpenAPI.

---

## Tecnologias utilizadas

- Python
- FastAPI
- Uvicorn
- SQLite
- Docker
- Swagger / OpenAPI

---

## Estrutura do projeto

```text
historico-enderecos-api/
│
├── app.py
├── database.py
├── Dockerfile
├── requirements.txt
├── README.md
└── .gitignore
```

### Arquivos principais

- `app.py` — implementação da API REST e suas rotas.
- `database.py` — configuração e operações relacionadas ao banco SQLite.
- `requirements.txt` — dependências Python necessárias.
- `Dockerfile` — configuração para execução da API em um contêiner Docker.

---

## Instalação e execução

### Pré-requisitos

Para executar o projeto localmente é necessário ter instalado:

- Git
- Python
- Docker

---

## Executar com Docker

Na pasta do projeto, construa a imagem:

```bash
docker build -t historico-enderecos-api .
```

Depois execute o contêiner:

```bash
docker run -p 8001:8001 historico-enderecos-api
```

A API ficará disponível em:

```text
http://127.0.0.1:8001
```

A documentação Swagger poderá ser acessada em:

```text
http://127.0.0.1:8001/docs
```

> Na execução completa do projeto, recomenda-se utilizar o `docker-compose.yml` disponível no repositório da API principal.

---

## Executar localmente com Python

Também é possível executar a API sem Docker.

### 1. Criar um ambiente virtual

```bash
python -m venv .venv
```

### 2. Ativar o ambiente virtual

No Windows:

```bash
.venv\Scripts\activate
```

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 4. Iniciar a API

```bash
uvicorn app:app --host 0.0.0.0 --port 8001
```

---

## Endpoints

### Listar histórico

```text
GET /historico
```

Retorna os endereços armazenados no histórico.

### Filtrar histórico

O histórico também pode ser filtrado por CEP, cidade e UF através de parâmetros opcionais.

Exemplos:

```text
GET /historico?cep=04007-004
GET /historico?cidade=São Paulo
GET /historico?uf=SP
```

Os filtros também podem ser combinados:

```text
GET /historico?cidade=São Paulo&uf=SP
```

Essa funcionalidade permite localizar registros específicos sem precisar retornar todo o histórico.

### Consultar registro

```text
GET /historico/{id}
```

Retorna um registro específico através do seu identificador.

### Adicionar endereço

```text
POST /historico
```

Adiciona um novo endereço ao histórico.

### Atualizar endereço

```text
PUT /historico/{id}
```

Atualiza um endereço existente.

### Excluir endereço

```text
DELETE /historico/{id}
```

Remove um endereço do histórico.

---

## Banco de dados

A aplicação utiliza SQLite para armazenar os registros.

Por padrão, quando executada localmente, a API utiliza:

```text
enderecos.db
```

Quando executada através do Docker Compose da API principal, é utilizada a variável:

```text
DATABASE_NAME=/app/data/enderecos.db
```

O banco é armazenado em um volume Docker, permitindo que os dados permaneçam disponíveis mesmo após a remoção e recriação dos contêineres.

---

## Integração com a API principal

A API principal envia os endereços consultados para este serviço.

Na execução através do Docker Compose, os serviços se comunicam através da rede:

```text
cep-network
```

A API secundária é identificada dentro dessa rede como:

```text
historico-api
```

A porta utilizada pelo serviço é:

```text
8001
```

---

## Funcionalidades

- Cadastro de endereços
- Consulta do histórico
- Consulta de registro por ID
- Filtros de histórico por CEP, cidade e UF
- Combinação de múltiplos filtros
- Atualização de endereços
- Exclusão de registros
- Persistência em SQLite
- Integração com a API principal
- Execução em contêiner Docker
- Documentação automática com Swagger/OpenAPI