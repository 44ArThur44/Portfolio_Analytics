from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from . import database, repository, services

router = APIRouter()


@router.post('/api/visit', status_code=201)
def post_visit(payload: dict, request: Request, db: Session = Depends(database.get_db)):
    # Determine client IP
    client_ip = None
    xff = request.headers.get('x-forwarded-for')
    if xff:
        client_ip = xff.split(',')[0].strip()
    else:
        client = request.client
        if client:
            client_ip = client.host

    ip_hash = services.anonymize_ip(client_ip)
    country = services.lookup_country(client_ip)
    user_agent = request.headers.get('user-agent')
    page = payload.get('page') if isinstance(payload, dict) else None

    ev = {
        'ip_hash': ip_hash,
        'country': country,
        'user_agent': user_agent,
        'page': page
    }
    saved = repository.insert_event(db, ev)
    return {'id': saved.id}


@router.get('/api/metrics')
def get_metrics(limit: int = 100, db: Session = Depends(database.get_db)):
    rows = repository.visits_by_country(db, limit=limit)
    return {'by_country': rows}
