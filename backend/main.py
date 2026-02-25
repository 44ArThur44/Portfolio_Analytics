from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from . import routers

def create_app() -> FastAPI:
    app = FastAPI(title='Portfolio Analytics')

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(routers.router)

    @app.on_event('startup')
    def startup():
        Base.metadata.create_all(bind=engine)

    return app

app = create_app()

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('backend.main:app', host='0.0.0.0', port=8000, reload=True)
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, database
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserCreate(BaseModel):
    name: str
    email: str


@app.on_event("startup")
def on_startup():
    database.Base.metadata.create_all(bind=database.engine)


@app.get('/api/users')
def list_users(db: Session = Depends(database.get_db)):
    return db.query(models.User).all()


@app.post('/api/users', status_code=201)
def create_user(payload: UserCreate, db: Session = Depends(database.get_db)):
    exists = db.query(models.User).filter(models.User.email == payload.email).first()
    if exists:
        raise HTTPException(status_code=400, detail='Email já cadastrado')
    u = models.User(name=payload.name, email=payload.email)
    db.add(u)
    db.commit()
    db.refresh(u)
    return u


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('backend.main:app', host='0.0.0.0', port=8000, reload=True)
