from sqlalchemy.orm import Session
from sqlalchemy import func
from . import models

def insert_event(db: Session, event: dict):
    e = models.Event(
        ip_hash=event.get('ip_hash'),
        country=event.get('country', 'ZZ'),
        user_agent=event.get('user_agent'),
        page=event.get('page')
    )
    db.add(e)
    db.commit()
    db.refresh(e)
    return e

def visits_by_country(db: Session, limit: int = 100):
    q = db.query(models.Event.country, func.count(models.Event.id).label('count'))
    q = q.group_by(models.Event.country).order_by(func.count(models.Event.id).desc()).limit(limit)
    return [{ 'country': r[0], 'count': r[1] } for r in q.all()]
