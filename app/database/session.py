import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL")


if DATABASE_URL.startswith('sqlite'):
    engine = create_engine(
        "sqlite:///mydatabase.db",
        connect_args={'check_same_thread': False},
        echo=True
    )
else:
    engine = create_engine("sqlite:///mydatabase.db")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Безопасное закрытие сессии даже при ошибках"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
