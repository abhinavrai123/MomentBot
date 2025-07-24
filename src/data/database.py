# src/data/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base
import os

# Load from .env or fallback
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///data/data.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = scoped_session(sessionmaker(bind=engine, autocommit=False, autoflush=False))

Base = declarative_base()

def init_db():
    from .models import LogEntry, MoodSwing
    Base.metadata.create_all(bind=engine)
