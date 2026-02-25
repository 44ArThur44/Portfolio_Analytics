"""
Minimal visit tracking backend.
FastAPI + SQLite in one file.
"""
import sqlite3
import json
from datetime import datetime
from typing import Optional
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import geoip2.database
import os

# ============================================================================
# Config
# ============================================================================
DB_FILE = 'visits.db'
GEOIP_DB = os.getenv('GEOIP_DB')  # Path to MaxMind GeoLite2-City.mmdb
GEOIP_READER = None

if GEOIP_DB and os.path.exists(GEOIP_DB):
    GEOIP_READER = geoip2.database.Reader(GEOIP_DB)

# ============================================================================
# Database setup
# ============================================================================
def init_db():
    """Create visits table if not exists."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS visits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            start_time TEXT NOT NULL,
            end_time TEXT,
            country TEXT,
            city TEXT,
            duration_seconds INTEGER,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# ============================================================================
# Geolocation helper
# ============================================================================
def get_location(ip: str) -> tuple:
    """Lookup country and city from IP. Returns ('XX', 'Unknown') if not found."""
    if not GEOIP_READER or not ip or ip == '127.0.0.1':
        return ('ZZ', 'Unknown')
    try:
        response = GEOIP_READER.city(ip)
        country = response.country.iso_code or 'ZZ'
        city = response.city.name or 'Unknown'
        return (country, city)
    except Exception:
        return ('ZZ', 'Unknown')

# ============================================================================
# FastAPI app
# ============================================================================
app = FastAPI(title='Visit Tracker')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# ============================================================================
# Pydantic models
# ============================================================================
class StartVisitRequest(BaseModel):
    pass

class StartVisitResponse(BaseModel):
    visit_id: int
    message: str

class EndVisitRequest(BaseModel):
    visit_id: int
    duration_seconds: int

class EndVisitResponse(BaseModel):
    message: str

class StatsResponse(BaseModel):
    total_visits: int
    avg_duration_seconds: Optional[float]
    visits_by_country: dict
    visits_by_city: dict

# ============================================================================
# Helpers
# ============================================================================
def get_client_ip(request):
    """Extract client IP from request."""
    xff = request.headers.get('x-forwarded-for')
    if xff:
        return xff.split(',')[0].strip()
    if request.client:
        return request.client.host
    return '0.0.0.0'

# ============================================================================
# Routes
# ============================================================================
@app.on_event('startup')
def startup():
    init_db()

@app.post('/api/start_visit', response_model=StartVisitResponse)
def start_visit(request_obj: StartVisitRequest, request: Request):
    """Start tracking a visit. Returns visit_id."""
    ip = get_client_ip(request)
    country, city = get_location(ip)
    now = datetime.utcnow().isoformat()
    
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute(
        'INSERT INTO visits (start_time, country, city) VALUES (?, ?, ?)',
        (now, country, city)
    )
    conn.commit()
    visit_id = c.lastrowid
    conn.close()
    
    return {
        'visit_id': visit_id,
        'message': f'Visit started from {country}/{city}'
    }

@app.post('/api/end_visit', response_model=EndVisitResponse)
def end_visit(payload: EndVisitRequest):
    """End a visit and record duration."""
    visit_id = payload.visit_id
    duration = payload.duration_seconds
    now = datetime.utcnow().isoformat()
    
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute(
        'UPDATE visits SET end_time = ?, duration_seconds = ? WHERE id = ?',
        (now, duration, visit_id)
    )
    conn.commit()
    conn.close()
    
    return {'message': f'Visit {visit_id} ended (duration: {duration}s)'}

@app.get('/api/stats', response_model=StatsResponse)
def get_stats():
    """Return aggregated visit stats."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    # Total visits
    c.execute('SELECT COUNT(*) FROM visits')
    total = c.fetchone()[0]
    
    # Average duration
    c.execute('SELECT AVG(duration_seconds) FROM visits WHERE duration_seconds IS NOT NULL')
    avg_duration = c.fetchone()[0]
    
    # Visits by country
    c.execute('SELECT country, COUNT(*) as cnt FROM visits GROUP BY country ORDER BY cnt DESC')
    by_country = {row[0]: row[1] for row in c.fetchall()}
    
    # Visits by city
    c.execute('SELECT city, COUNT(*) as cnt FROM visits GROUP BY city ORDER BY cnt DESC')
    by_city = {row[0]: row[1] for row in c.fetchall()}
    
    conn.close()
    
    return {
        'total_visits': total,
        'avg_duration_seconds': avg_duration,
        'visits_by_country': by_country,
        'visits_by_city': by_city
    }

# ============================================================================
# Health check
# ============================================================================
@app.get('/health')
def health():
    return {'status': 'ok'}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
