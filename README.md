# Gym API

API REST desenvolvida com Flask para gerenciamento de uma academia.

O projeto possui 3 recursos principais:
- Alunos
- Treinos
- Pagamentos

Cada recurso possui operacoes de CRUD.

## Tecnologias

- Python 3
- Flask
- Flask-SQLAlchemy
- Flask-Cors
- SQLite

## Estrutura

```text
gym_api/
|-- app.py
|-- models.py
|-- requirements.txt
|-- README.md
`-- routes/
    |-- aluno_routes.py
    |-- treino_routes.py
    `-- pagamentos_routes.py
```

## Como executar

1. Clone o repositorio:

```bash
git clone https://github.com/Thales1914/gym_api.git
cd gym_api
```

2. Instale as dependencias:

```bash
pip install -r requirements.txt
```

3. Execute a aplicacao:

```bash
python app.py
```

4. A API ficara disponivel em:

```text
http://127.0.0.1:5000
```

O banco SQLite e criado automaticamente ao iniciar a aplicacao.

## Teste rapido

Endpoint inicial:

```http
GET /
```

Resposta esperada:

```json
{
  "mensagem": "GymAPI funcionando com sucesso!"
}
```

## Testando no Insomnia

Base URLs:

```text
Local: http://127.0.0.1:5000
Deploy: https://gym-api-vf6c.onrender.com
```

Para requisicoes `POST` e `PUT`, use `Body > JSON`.

### Exemplo 1: criar aluno

```http
POST /alunos/
```

```json
{
  "nome": "Thales",
  "email": "thales@test.com",
  "idade": 25,
  "telefone": "11999999999"
}
```

### Exemplo 2: criar treino

```http
POST /treinos/
```

```json
{
  "nome": "Treino A",
  "descricao": "Peito e triceps",
  "duracao": "45 min",
  "nivel": "iniciante",
  "instrutor": "Carlos"
}
```

### Exemplo 3: criar pagamento

```http
POST /pagamentos/
```

```json
{
  "aluno_id": 1,
  "valor": 99.9,
  "data_pagamento": "2026-04-09",
  "status": "pago",
  "metodo": "pix"
}
```

Observacao:
Se um aluno possuir pagamentos vinculados, a exclusao do aluno retorna `409 Conflict`.

## Endpoints

### Alunos

- `POST /alunos/` cria um aluno
- `GET /alunos/` lista todos os alunos
- `GET /alunos/<id>` busca um aluno por id
- `PUT /alunos/<id>` atualiza um aluno
- `DELETE /alunos/<id>` remove um aluno

### Treinos

- `POST /treinos/` cria um treino
- `GET /treinos/` lista todos os treinos
- `GET /treinos/<id>` busca um treino por id
- `PUT /treinos/<id>` atualiza um treino
- `DELETE /treinos/<id>` remove um treino

### Pagamentos

- `POST /pagamentos/` cria um pagamento
- `GET /pagamentos/` lista todos os pagamentos
- `GET /pagamentos/<id>` busca um pagamento por id
- `PUT /pagamentos/<id>` atualiza um pagamento
- `DELETE /pagamentos/<id>` remove um pagamento

## Modelagem dos recursos

### Aluno

- `id`
- `nome`
- `email`
- `idade`
- `telefone`

### Treino

- `id`
- `nome`
- `descricao`
- `duracao`
- `nivel`
- `instrutor`

### Pagamento

- `id`
- `aluno_id`
- `valor`
- `data_pagamento`
- `status`
- `metodo`

## Deploy

Deploy publico:

```text
https://gym-api-vf6c.onrender.com
```
