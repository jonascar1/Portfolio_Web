# Portfólio Web + Microserviço de Notificações

Projeto acadêmico composto por **dois projetos Django independentes** que se comunicam entre si:

- **Portfolio Web** — exibe informações pessoais, projetos e certificados. Possui API REST com autenticação JWT e integração com o microserviço de notificações. Roda na porta **8000**.
- **Microserviço de Notificações** — serviço independente responsável por criar e gerenciar notificações via API REST. Roda na porta **8001**.

> Cada projeto tem sua **própria venv** e deve ser executado em um **terminal separado**.

---

## Tecnologias Utilizadas

<p align="left">
  <img src="https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white"/>
  <img src="https://img.shields.io/badge/Django_REST_Framework-API-red?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/JWT-Autenticação-black?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite&logoColor=white"/>
  <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white"/>
  <img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white"/>
  <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black"/>
</p>

---

## 1. Clonar os repositórios

```bash
git clone https://github.com/jonascar1/Portfolio_Web.git
git clone https://github.com/jonascar1/Microservico-Notificacao.git
```

Você terá duas pastas:

```
Portfolio_Web/
Microservico-Notificacao/
```

---

## 2. Configurar o Microserviço de Notificações

Abra um terminal e entre na pasta do microserviço:

```bash
cd Microservico-Notificacao
```

Crie e ative a virtualenv **deste projeto**:

```bash
python3 -m venv venv
source venv/bin/activate
```

> **Obs.:** Em algumas distribuições Linux, o comando pode ser `python` em vez de `python3`. Verifique com `python --version` ou `python3 --version`.

Instale as dependências:

```bash
pip install -r requirements.txt
```

Agora **entre na subpasta** do projeto Django:

```bash
cd notificacao_ms
```

Aplique as migrations:

```bash
python manage.py migrate
```

Crie um superusuário (necessário para acessar o Admin):

```bash
python manage.py createsuperuser
```

Siga as instruções: informe usuário, e-mail e senha.

---

## 3. Obter a API Key do Microserviço

Inicie o servidor do microserviço (continue na pasta `notificacao_ms`):

```bash
python manage.py runserver 8001
```

Acesse o painel Admin em: [http://127.0.0.1:8001/admin/](http://127.0.0.1:8001/admin/)

Faça login com o superusuário criado e:

1. Acesse **Empresas** → **Adicionar Empresa**
2. Preencha o nome e salve
3. Após salvar, será gerado um **hash** automaticamente para essa empresa
4. **Copie esse hash** — ele será usado como `NOTIFICACAO_MS_API_KEY` no Portfolio

> Mantenha o microserviço rodando neste terminal durante todo o uso do sistema.

---

## 4. Configurar o Portfolio Web

Abra um **novo terminal** e entre na pasta do Portfolio:

```bash
cd Portfolio_Web
```

Crie e ative a venv **deste projeto** (separada da anterior):

```bash
python3 -m venv venv
source venv/bin/activate
```

> **Obs.:** Em algumas distribuições Linux, o comando pode ser `python` em vez de `python3`.

Instale as dependências:

```bash
pip install -r requirements.txt
```

Agora **entre na subpasta** do projeto Django:

```bash
cd PORTFOLIO_WEB
```

Aplique as migrations:

```bash
python manage.py migrate
```

Crie um superusuário (necessário para acessar o Admin):

```bash
python manage.py createsuperuser
```

Siga as instruções: informe usuário, e-mail e senha.

---

## 5. Configurar a Integração no Portfolio

Abra o arquivo `config/settings.py` e localize (ou adicione) as seguintes linhas:

```python
NOTIFICACAO_MS_URL = "http://127.0.0.1:8001"
NOTIFICACAO_MS_API_KEY = "COLE_AQUI_O_HASH_DA_EMPRESA"
```

Substitua `COLE_AQUI_O_HASH_DA_EMPRESA` pelo hash copiado no passo anterior.

> Essa API Key é enviada automaticamente no header `X-Api-Key` a cada requisição do Portfolio para o microserviço.

---

## 6. Iniciar o Portfolio Web

Ainda no terminal do Portfolio, com a venv ativada (na pasta raiz do Portfolio):

```bash
python manage.py runserver 8000
```

Acesse o Portfolio em: [http://127.0.0.1:8000/portfolio/](http://127.0.0.1:8000/portfolio/)

---

## Ordem de Execução (Resumo)

### Terminal 1 - Microserviço

```bash
cd Microservico-Notificacao
source venv/bin/activate
cd notificacao_ms
python manage.py runserver 8001
```

**URL:** http://127.0.0.1:8001

### Terminal 2 - Portfolio

```bash
cd Portfolio_Web
source venv/bin/activate
python manage.py runserver 8000
```

**URL:** http://127.0.0.1:8000

O microserviço **deve estar rodando antes** do Portfolio ser acessado.

---

## Testando o Sistema

### Autenticação JWT (Portfolio)

Obtenha um token de acesso enviando suas credenciais:

```bash
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "seu_usuario", "password": "sua_senha"}'
```

Resposta esperada:

```json
{
  "access": "eyJ...",
  "refresh": "eyJ..."
}
```

Para renovar o token:

```bash
curl -X POST http://127.0.0.1:8000/api/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh": "SEU_REFRESH_TOKEN"}'
```

---

### Criar uma Notificação

É possível criar tanto pela interface Admin quanto pela API.

#### Via API (curl):

```bash
curl -X POST http://127.0.0.1:8001/api/notificacoes/criar/ \
  -H "Content-Type: application/json" \
  -H "X-Api-Key: HASH_DA_EMPRESA" \
  -d '{
    "user_id": 1,
    "titulo": "Notificação de teste",
    "mensagem": "Conteúdo da notificação"
  }'
```

> Substitua `HASH_DA_EMPRESA` pelo hash gerado e `user_id` pelo ID do usuário cadastrado no Portfolio.

#### Via Admin do Microserviço:

Acesse [http://127.0.0.1:8001/admin/](http://127.0.0.1:8001/admin/) e:

1. Acesse **Notificações** → **Adicionar Notificação**
2. Informe a empresa (previamente cadastrada)
3. Informe o título e o conteúdo
4. Salve

---

### Testando o Sino de Notificações

1. Acesse o Portfolio em [http://127.0.0.1:8000/](http://127.0.0.1:8000/) e faça login
2. Crie uma notificação via API ou Admin (conforme acima)
3. O ícone de sino deve exibir o contador de notificações não lidas
4. Clique no sino para listar as notificações
5. Ao clicar em uma notificação, ela é marcada como lida automaticamente via JavaScript

---

## Endpoints de Referência

### Portfolio (porta 8000)

| Método | Endpoint              | Descrição                          |
|--------|-----------------------|------------------------------------|
| POST   | `/api/token/`         | Obter tokens JWT (access + refresh)|
| POST   | `/api/token/refresh/` | Renovar token de acesso            |

### Microserviço (porta 8001)

| Método | Endpoint                         | Descrição                    | Auth       |
|--------|----------------------------------|------------------------------|------------|
| POST   | `/api/notificacoes/criar/`       | Criar nova notificação       | X-Api-Key  |
| GET    | `/api/notificacoes/`             | Listar notificações          | X-Api-Key  |
| GET    | `/api/notificacoes/nao-lidas/`   | Contagem de não lidas        | X-Api-Key  |
| PATCH  | `/api/notificacoes/<id>/lida/`   | Marcar notificação como lida | X-Api-Key  |

---
