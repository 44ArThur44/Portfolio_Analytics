# Portfolio + Visit Tracker

Backend em **FastAPI** com **SQLite** para rastrear visitas.

## Como funciona

### Backend (`app.py`)

Um arquivo único com 3 endpoints principais:

| Endpoint           | Método | O que faz                                |
| ------------------ | ------ | ---------------------------------------- |
| `/health`          | GET    | Verifica se o backend está rodando       |
| `/api/start_visit` | POST   | Inicia uma visita, retorna `visit_id`    |
| `/api/end_visit`   | POST   | Finaliza visita com tempo gasto          |
| `/api/stats`       | GET    | Mostra total de visitas e média de tempo |

### O que é rastreado

- **Country + City**: obtido do IP do visitante
- **Timestamp**: hora exata da visita
- **Duração**: quantos segundos o usuário ficou na página
- **User-Agent**: navegador/dispositivo

### Banco de dados

# Guia do Projeto: Backend & Banco de Dados

## 1. Linguagem e Framework

O backend usa **Python** com o framework **FastAPI**. FastAPI é rápido, fácil de usar e ideal para APIs modernas.

## 2. Conexão com Banco de Dados (PostgreSQL)

O backend conecta ao **PostgreSQL** usando SQLAlchemy. A URL do banco deve ser definida na variável de ambiente `DATABASE_URL`:

```
export DATABASE_URL="postgresql://usuario:senha@localhost:5432/nome_do_banco"
```

Se não definir, ele usa um padrão local PostgreSQL. Não há fallback para SQLite.

## 3. Endpoints Disponíveis

| Endpoint           | Método | O que faz                                 | Exemplo de uso |
|--------------------|--------|-------------------------------------------|----------------|
| `/api/users`       | GET    | Lista todos os usuários                   | curl http://localhost:8000/api/users |
| `/api/users`       | POST   | Cria um novo usuário                      | curl -X POST http://localhost:8000/api/users -H 'Content-Type: application/json' -d '{"name": "João", "email": "joao@email.com"}' |
| `/api/visit`       | POST   | Registra uma visita (analytics)           | curl -X POST http://localhost:8000/api/visit -H 'Content-Type: application/json' -d '{"page": "/home"}' |
| `/api/metrics`     | GET    | Retorna métricas de visitas por país      | curl http://localhost:8000/api/metrics |

## 4. Estrutura dos Arquivos do Backend

```
backend/
├── main.py        # Inicializa o FastAPI, rotas e banco
├── database.py    # Conexão e sessão com PostgreSQL
├── models.py      # Modelos/tabelas do banco (User, Event)
├── routers.py     # Rotas da API (visit, metrics)
├── repository.py  # Funções para gravar/buscar dados
├── services.py    # Regras de negócio (ex: anonimizar IP, GeoIP)
└── migrations/    # Scripts SQL para criar tabelas
```

## 5. Como Rodar o Backend Localmente

```bash
cd '/home/arthur/Documentos/web 2.0'
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export DATABASE_URL="postgresql://usuario:senha@localhost:5432/nome_do_banco"
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

## 6. Dicas de Deploy Gratuito e Possíveis Problemas

- Para deploy gratuito, use serviços como Render, Railway ou Heroku (PostgreSQL incluso).
- Se a variável `DATABASE_URL` não estiver correta, o backend não salva dados e pode dar erro ao iniciar.
- O banco precisa existir e estar acessível.

## 7. Observações sobre SQLite e PostgreSQL

- O backend foi migrado para **PostgreSQL** por ser mais robusto e escalável.
- Não há fallback automático para SQLite.
- Se quiser usar SQLite para testes, altere manualmente a string de conexão, mas o padrão é PostgreSQL.

## 8. Fluxo de Dados Básico

- O frontend envia visitas para `/api/visit`.
- O backend coleta: hash do IP (anonimizado), país (via GeoIP), user-agent e página visitada.
- Esses dados são gravados na tabela `events`.
- Métricas podem ser consultadas em `/api/metrics`.

## 9. Configurações Extras

- Para GeoIP, defina a variável `GEOIP_DB` com o caminho do arquivo MaxMind `.mmdb`:
  ```bash
  export GEOIP_DB="/caminho/para/GeoLite2-City.mmdb"
  ```
- A variável `VISIT_SALT` pode ser usada para customizar o hash do IP.

## Referência Rápida dos Endpoints

```bash
# Listar usuários
curl http://localhost:8000/api/users

# Criar usuário
curl -X POST http://localhost:8000/api/users -H 'Content-Type: application/json' -d '{"name": "João", "email": "joao@email.com"}'

# Registrar visita
curl -X POST http://localhost:8000/api/visit -H 'Content-Type: application/json' -d '{"page": "/home"}'

# Consultar métricas
curl http://localhost:8000/api/metrics
```

---

## Frontend (Resumo)

- O frontend estático está em `frontend/`.
- Basta abrir `index.html` no navegador ou rodar:
  ```bash
  cd frontend
  python3 -m http.server 8080
  ```
- Ele consome as APIs do backend para mostrar dados e registrar visitas.

---

**Sempre confira a variável `DATABASE_URL` e o arquivo de GeoIP para evitar erros!**
2. Chama `/api/end_visit` quando o usuário sai (beforeunload)
