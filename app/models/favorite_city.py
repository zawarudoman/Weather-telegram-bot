from sqlalchemy import Column, Integer, String, DateTime, Boolean, MetaData, ForeignKey, re
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.session import Base, engine, SessionLocal
from app.models.user import User


metadata = MetaData()


class FavoriteCity(Base):
    __tablename__ = 'favorite_city'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    city_name = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now)

    user = relationship('User', back_populates='favorite_city')
