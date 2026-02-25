# Copilot instructions for this repository

Resumo rápido

- Arquitetura: frontend estático em `frontend/` (HTML/CSS/JS). Backend API em `backend/` usando FastAPI (`backend/main.py`). Banco com SQLAlchemy em `backend/database.py` e modelos em `backend/models.py`.
- Fluxo de dados: o frontend faz fetch para `/api/users` (ver `frontend/script.js`). O backend expõe `GET /api/users` e `POST /api/users` (ver `backend/main.py`).

O que é essencial para a IA saber

- Entradas/saídas claro: `POST /api/users` espera JSON {"name": "...", "email": "..."} e retorna o recurso criado (201). `GET /api/users` retorna lista de usuários.
- Banco: a URL do PostgreSQL vem de `DATABASE_URL` (variável de ambiente) com fallback em `backend/database.py` — ajuste antes de rodar.
- Migração: o projeto usa `Base.metadata.create_all(...)` em evento `startup` (não há sistema de migrações como Alembic).
- Dependências: listadas em `requirements.txt` (FastAPI, uvicorn, SQLAlchemy, psycopg2-binary).

Padrões e convenções do projeto

- DB sessions: use o dependency `get_db()` em `backend/database.py` (gera um session via yield). Ao implementar handlers, aceite `db: Session = Depends(database.get_db)`.
- Modelos: `backend/models.py` define `User` com `id, name, email` — email é único.
- Criação de esquema: o app chama `database.Base.metadata.create_all(bind=database.engine)` na inicialização — alterações no modelo exigem recriar o DB ou usar migrações manuais.
- CORS: o backend permite todas origens (`allow_origins=["*"]`) em `backend/main.py` — mudanças no comportamento de CORS devem ser feitas aí.

Dev / executar / debug (comandos específicos)

- Instalar dependências:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

- Rodar a API (desenvolvimento):

```bash
export DATABASE_URL="postgresql://user:password@localhost:5432/mydb"
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

- Servir frontend localmente (opções):
  - Abrir `frontend/index.html` direto no navegador (simples), ou
  - Servir com um HTTP simples: `python3 -m http.server 8080` dentro da pasta `frontend/` e abrir `http://localhost:8080`.

Padrões de implementação desejados (exemplos do código)

- Ao adicionar endpoints, siga o padrão em `backend/main.py`: use Pydantic `BaseModel` para payloads, retornar modelos SQLAlchemy convertidos automaticamente pelo FastAPI.
- Para operações de DB: ver `create_user` — verificar unicidade por e-mail antes de inserir e usar `db.commit()` + `db.refresh()`.

Integrações e pontos de atenção

- O frontend chama a rota relativa `/api/users` (ver `frontend/script.js`). Se servir o frontend por outro host, ajuste `API_BASE` ou CORS.
- A configuração do banco é obrigatória para operações que tocam o DB; sem `DATABASE_URL` apontando para um PostgreSQL válido o app não persistirá dados.

Arquivos chave para referência rápida

- `backend/main.py` — rotas e inicialização
- `backend/database.py` — engine, `SessionLocal`, `get_db()`
- `backend/models.py` — modelos SQLAlchemy
- `frontend/script.js` — consumo das APIs
- `README.md`, `requirements.txt`

Perguntas que você pode fazer ao humano

- Deseja que eu sirva o frontend via FastAPI (integração estática)?
- Prefere que eu adicione Dockerfile/docker-compose para PostgreSQL + app?

Se algo estiver faltando ou impreciso, peça exemplos de código ou esclareça como o autor costuma rodar o projeto.
