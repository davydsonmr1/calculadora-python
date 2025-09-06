# Calculadora Python API - trabalho 05-09-2024 - Davydson Maciel

API RESTful com FastAPI que foi desenvolvida no curso técnico de desenvolvimento de sitemas. Oferece funcionalidades de calculadora e integração com ViaCEP para consulta de endereços no cadastro de usuários.

## Estrutura do Projeto

```
calculadora_python/
| --app/
|  | --__init__.py
|  | --main.py
|  | --config.py
|  | --auth.py
|  | --database.py
|  | --models.py
|  | --viacep.py
|  | --routers/
|  |   | -- __init__.py
|  |   | -- calculadora.py
|  |   | -- usuarios.py
|  |   | -- viacep.py
|--requirements.txt
|--readme.md
```

## Funcionalidades

### Calculadora
- Operações básicas: soma, subtração, multiplicação e divisão
- Cálculo de raiz n-ésima

### Usuários
- Cadastro de usuários com integração de endereço via CEP
- Login com autenticação JWT
- Proteção de rotas por autenticação

### ViaCEP
- Consulta de endereços a partir do CEP
- Integração automática no cadastro de usuários

## Tecnologias Utilizadas

- **FastAPI**: Framework web para criação de APIs
- **PyMongo**: Conexão com MongoDB
- **ViaCEP API**: Serviço para consulta de endereços
- **Python-Jose**: Implementação JWT para autenticação
- **Requests**: Biblioteca para requisições HTTP

## Instalação

1. Clone este repositório:
   ```
   git clone https://github.com/davydsonmr1/calculadora-python.git
   cd calculadora-python
   ```

2. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

3. Certifique-se de ter o MongoDB instalado e em execução em `localhost:27017`

4. Execute a API:
   ```
   python -m uvicorn app.main:app --reload
   ```

## Como Testar

### Testando a API de Endereços (ViaCEP)

1. Primeiro, faça login para obter um token:
   ```
   curl -X 'POST' \
     'http://localhost:8000/usuarios/login' \
     -H 'Content-Type: application/json' \
     -d '{
       "username": "seu_usuario",
       "password": "sua_senha"
     }'
   ```

2. Consulte um CEP diretamente:
   ```
   curl -X 'GET' \
     'http://localhost:8000/viacep/cep/01310100' \
     -H 'Authorization: Bearer SEU_TOKEN'
   ```

3. Cadastre um novo usuário com preenchimento automático de endereço:
   ```
   curl -X 'POST' \
     'http://localhost:8000/usuarios/registro' \
     -H 'Content-Type: application/json' \
     -H 'Authorization: Bearer SEU_TOKEN' \
     -d '{
       "username": "novo_usuario",
       "password": "senha123",
       "cep": "01310100",
       "numero": "123",
       "complemento": "Sala 456"
     }'
   ```

### Interface Swagger

Você também pode testar todas as funcionalidades através da interface Swagger:

1. Acesse `http://localhost:8000/docs` em seu navegador
2. Faça login através da rota `/usuarios/login` para obter um token
3. Clique no botão "Authorize" no topo da página e insira `Bearer SEU_TOKEN`
4. Teste as rotas disponíveis, incluindo o cadastro de usuários com CEP

## Novidades

### Integração ViaCEP no Cadastro de Usuários

A aplicação agora preenche automaticamente os dados de endereço durante o cadastro de usuários:

- O usuário informa apenas o CEP, número e complemento
- A API ViaCEP é consultada para obter logradouro, bairro, cidade e UF
- O endereço completo é armazenado junto com os dados do usuário
- Em caso de CEP inválido, a API retorna erro apropriado