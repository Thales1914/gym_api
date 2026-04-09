# Relatorio - Trabalho 05 AV2

## Tema do sistema

O sistema desenvolvido foi uma API REST para gerenciamento de academia.

O dominio escolhido foi academia porque permite modelar entidades comuns em sistemas reais, com relacionamento entre recursos e operacoes frequentes de cadastro, consulta, atualizacao e remocao.

## Tecnologias utilizadas

- Python
- Flask
- Flask-SQLAlchemy
- Flask-Cors
- SQLite
- Gunicorn
- Render

## Descricao do sistema

A aplicacao permite o gerenciamento de tres recursos principais:
- Alunos
- Treinos
- Pagamentos

O objetivo da API e centralizar o cadastro de alunos da academia, os treinos disponiveis e os pagamentos realizados pelos alunos.

## Modelagem dos recursos

### Aluno

- `id`: inteiro, chave primaria
- `nome`: string, obrigatorio
- `email`: string, obrigatorio e unico
- `idade`: inteiro, obrigatorio
- `telefone`: string, obrigatorio

### Treino

- `id`: inteiro, chave primaria
- `nome`: string, obrigatorio
- `descricao`: string, obrigatorio
- `duracao`: string, obrigatorio
- `nivel`: string, obrigatorio
- `instrutor`: string, obrigatorio

### Pagamento

- `id`: inteiro, chave primaria
- `aluno_id`: inteiro, chave estrangeira para `Aluno`
- `valor`: float, obrigatorio
- `data_pagamento`: string, obrigatorio
- `status`: string, obrigatorio
- `metodo`: string, obrigatorio

## Relacionamentos

- Um aluno pode possuir varios pagamentos.
- Cada pagamento pertence a um unico aluno.
- O recurso treino nao possui relacionamento direto com os demais recursos nesta versao do sistema.

## Documentacao dos endpoints

Base URL local:

```text
http://127.0.0.1:5000
```

Base URL de deploy:

```text
https://gym-api-vf6c.onrender.com
```

### Recurso Alunos

#### `POST /alunos/`

Corpo da requisicao:

```json
{
  "nome": "Thales",
  "email": "thales85@test.com",
  "idade": 22,
  "telefone": "85999999999"
}
```

Resposta esperada:
- `201 Created` com o objeto criado
- `400 Bad Request` em caso de JSON ausente ou email duplicado

#### `GET /alunos/`

Resposta esperada:
- `200 OK` com lista de alunos

#### `GET /alunos/<id>`

Resposta esperada:
- `200 OK` com o aluno encontrado
- `404 Not Found` se o aluno nao existir

#### `PUT /alunos/<id>`

Corpo da requisicao:

```json
{
  "nome": "Thales Barbosa",
  "idade": 23,
  "telefone": "85988888888"
}
```

Resposta esperada:
- `200 OK` com o objeto atualizado
- `404 Not Found` se o aluno nao existir

#### `DELETE /alunos/<id>`

Resposta esperada:
- `200 OK` com mensagem de sucesso
- `404 Not Found` se o aluno nao existir
- `409 Conflict` se o aluno possuir pagamentos vinculados

### Recurso Treinos

#### `POST /treinos/`

Corpo da requisicao:

```json
{
  "nome": "Treino A",
  "descricao": "Peito e triceps",
  "duracao": "45 min",
  "nivel": "iniciante",
  "instrutor": "Carlos"
}
```

Resposta esperada:
- `201 Created` com o objeto criado
- `400 Bad Request` em caso de JSON ausente ou campos faltando

#### `GET /treinos/`

Resposta esperada:
- `200 OK` com lista de treinos

#### `GET /treinos/<id>`

Resposta esperada:
- `200 OK` com o treino encontrado
- `404 Not Found` se o treino nao existir

#### `PUT /treinos/<id>`

Corpo da requisicao:

```json
{
  "nivel": "intermediario",
  "duracao": "50 min"
}
```

Resposta esperada:
- `200 OK` com o objeto atualizado
- `404 Not Found` se o treino nao existir

#### `DELETE /treinos/<id>`

Resposta esperada:
- `200 OK` com mensagem de sucesso
- `404 Not Found` se o treino nao existir

### Recurso Pagamentos

#### `POST /pagamentos/`

Corpo da requisicao:

```json
{
  "aluno_id": 1,
  "valor": 99.9,
  "data_pagamento": "2026-04-09",
  "status": "pago",
  "metodo": "pix"
}
```

Resposta esperada:
- `201 Created` com o objeto criado
- `400 Bad Request` em caso de JSON ausente ou campos faltando
- `404 Not Found` se o aluno informado nao existir

#### `GET /pagamentos/`

Resposta esperada:
- `200 OK` com lista de pagamentos

#### `GET /pagamentos/<id>`

Resposta esperada:
- `200 OK` com o pagamento encontrado
- `404 Not Found` se o pagamento nao existir

#### `PUT /pagamentos/<id>`

Corpo da requisicao:

```json
{
  "status": "pendente",
  "metodo": "cartao"
}
```

Resposta esperada:
- `200 OK` com o objeto atualizado
- `404 Not Found` se o pagamento nao existir

#### `DELETE /pagamentos/<id>`

Resposta esperada:
- `200 OK` com mensagem de sucesso
- `404 Not Found` se o pagamento nao existir

## URL de acesso ao deploy

```text
https://gym-api-vf6c.onrender.com
```

## Repositorio GitHub

```text
https://github.com/Thales1914/gym_api
```

## Divisao de tarefas

Divisao descrita com base no historico de commits do repositorio:

- Thales: estrutura inicial do projeto, configuracao principal da aplicacao, CRUD de alunos, atualizacao do README, ajustes finais de compatibilidade no recebimento de JSON e suporte ao deploy no Render
- Davi Almeida: implementacao das rotas e do CRUD de pagamentos
- LauanMo: implementacao das rotas e do CRUD de treinos, incluindo correcoes associadas

## Dificuldades encontradas e solucoes adotadas

- Diferenca no nome do arquivo de pagamentos e no import principal da aplicacao. Solucao: ajustar o import para `pagamentos_routes`.
- Erro `415 Unsupported Media Type` durante os testes no Insomnia. Solucao: melhorar a leitura do corpo JSON nas rotas para aceitar requisicoes mesmo com cabecalho inconsistente.
- Exclusao de aluno com pagamentos vinculados gerava erro de integridade no banco. Solucao: retornar `409 Conflict` quando houver pagamentos associados.
- Necessidade de disponibilizar a API publicamente. Solucao: adicionar `gunicorn` nas dependencias e realizar deploy no Render.

## Conclusao

O projeto atende ao objetivo de disponibilizar uma API REST com tres recursos, CRUD completo, persistencia em banco de dados e deploy publico para acesso externo.
