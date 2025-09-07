import os
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import create_engine

DB_PATH = os.path.join("data", "app.db")
os.makedirs("data", exist_ok=True)
engine = create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

class Base(DeclarativeBase):
    pass
