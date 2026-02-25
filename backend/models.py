from sqlalchemy import Column, Integer, String, Text, TIMESTAMP
from sqlalchemy.sql import func
from .database import Base

class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True, index=True)
    ts = Column(TIMESTAMP(timezone=True), server_default=func.now(), index=True)
    ip_hash = Column(String(128), nullable=False, index=True)
    country = Column(String(2), nullable=False, index=True)
    user_agent = Column(Text, nullable=True)
    page = Column(String(512), nullable=True)
from sqlalchemy import Column, Integer, String
from .database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
