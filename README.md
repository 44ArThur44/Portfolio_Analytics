# Portfolio + Analytics

Este projeto inclui um frontend estático em `frontend/` e um backend FastAPI opcional para analytics. O site pode funcionar sem o backend; a API só é necessária quando a coleta de visitas estiver habilitada em produção.

## Estrutura

- `frontend/`: portfolio estático
- `backend/main.py`: aplicação FastAPI principal para analytics
- `backend/database.py`: conexão com PostgreSQL via SQLAlchemy
- `backend/models.py`: modelos `Event` e `User`
- `backend/routers.py`: endpoints da API
- `backend/services.py`: anonimização de IP e lookup de país
- `app.py`: tracker mínimo, separado e não necessário para o deploy principal do portfolio

## Variáveis de ambiente

As variáveis realmente relevantes para o backend são:

```bash
export DATABASE_URL="postgresql://user:password@host:5432/dbname"
export GEOIP_DB="/caminho/para/GeoLite2-City.mmdb"   # opcional
export VISIT_SALT="change-me"                         # opcional
```

- `DATABASE_URL`: obrigatória para o backend funcionar com PostgreSQL.
- `GEOIP_DB`: opcional; habilita lookup de país com GeoIP.
- `VISIT_SALT`: opcional; personaliza o hash do IP para anonimização.

## Endpoints principais

- `POST /api/visit`: registra uma visita do frontend
- `GET /api/metrics`: retorna métricas por país
- `GET /health`: health check disponível no tracker mínimo em `app.py`

## Deploy

- O frontend pode ser publicado como site estático.
- O backend FastAPI é opcional e deve ser implantado apenas quando analytics estiver ativado.
- O backend exige PostgreSQL configurado e acessível via `DATABASE_URL`.
- Em produção, o app deve iniciar com:

```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

A aplicação cria as tabelas automaticamente no startup com `Base.metadata.create_all(...)`.

## Checklist de prontidão para deploy

- [ ] Dependências instaladas
- [ ] `DATABASE_URL` configurada
- [ ] PostgreSQL disponível e acessível
- [ ] Health check respondendo
- [ ] API funcionando
- [ ] Frontend integrado ao backend (somente se analytics estiver habilitado)

## Observações

- O frontend funciona independentemente do backend.
- O backend usa PostgreSQL.
- O tracker em `app.py` é um componente separado e não é obrigatório para o deployment do portfolio.

—> Para deploy em produção, o ponto crítico é a configuração correta do banco e das variáveis de ambiente.

