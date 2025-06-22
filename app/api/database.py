from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Generator
import sys
import os

# Добавляем путь к корню проекта
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from config import settings

DATABASE_URL = settings.DATABASE_URL
SQLALCHEMY_DATABASE_URL = DATABASE_URL

# Настройка engine в зависимости от типа базы данных
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db() -> Generator:
    """
    Функция-зависимость для получения сессии базы данных.
    Используется в FastAPI для внедрения зависимости базы данных.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

