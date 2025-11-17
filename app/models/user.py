from sqlalchemy import Column, Integer, String, DateTime, Boolean, MetaData
from sqlalchemy.sql import func
from app.database.session import Base, engine, SessionLocal


metadata = MetaData()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, index=True)
    username = Column(String, unique=True, nullable=True)
    first_name = Column(String)
    last_name = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    active_user = Column(Boolean, default=True)

    def __repr__(self):
        return f'<<User: telegram_id={self.telegram_id}, username:{self.username}, active={self.active_user}'

    @staticmethod
    def create(telegram_id: int, username: str, first_name: str, last_name: str):
        user = User(
            telegram_id=telegram_id,
            username=username,
            first_name=first_name,
            last_name=last_name
        )
        db = SessionLocal()
        db.add(user)
        db.commit()
        return user


metadata.create_all(engine)