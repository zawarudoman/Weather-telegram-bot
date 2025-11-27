from sqlalchemy import Column, Integer, String, DateTime, Boolean, MetaData
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.session import Base, engine, SessionLocal
from app.models.favorite_city import FavoriteCity

metadata = MetaData()


class User(Base):
    """
    Модель пользователя
    """
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, index=True)
    username = Column(String, unique=True, nullable=True)
    first_name = Column(String)
    last_name = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    active_user = Column(Boolean, default=True)
    language = Column(String, default='ru')
    units = Column(String, default='metric')
    notifications_enable = Column(Boolean, default=False)
    notifications_time = Column(DateTime, default='08:00')

    favorite_city = relationship('FavoriteCity', back_populates='user')  # связь с таблицей favorite_city

    def __repr__(self):
        return f'<<User: telegram_id={self.telegram_id}, username:{self.username}, active={self.active_user}'

    @staticmethod
    def get_or_create(telegram_id: int, username: str, first_name: str, last_name: str):
        """
        Создание пользователя
        :param telegram_id: уникальный id в телеграме
        :param username: уникальный username из телеграмма
        :param first_name: Имя
        :param last_name: фамилия (не обязательный параметр)
        :return: User (запись из таблицы с созданным пользователем)
        """

        db = SessionLocal()
        user = db.query(User).filter(User.telegram_id)
        if user:
            print('Юзер существует')
            return user
        else:
            user = User(
                telegram_id=telegram_id,
                username=username,
                first_name=first_name,
                last_name=last_name
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        return user

    @staticmethod
    def delete_user(telegram_id: int):
        """
        Удаление пользователя из базы

        :param telegram_id:
        :return: Удаленный пользователь, получаем подтверждение в консоль
        """
        db = SessionLocal()
        user = db.query(User).filter(User.telegram_id == telegram_id).first()
        if user is not None:
            db.delete(user)
            db.commit()
            return print('User удален')
        else:
            return print('User не существует')

    @staticmethod
    def get_favorite_cities(user_id: int):
        """Получить все любимые города пользователя"""
        db = SessionLocal()
        return db.query(FavoriteCity).filter(FavoriteCity.user_id == user_id).all()

    @staticmethod
    def add_favorite_city(user_id: int, city_name: str):
        db = SessionLocal()
        existing_city = db.query(FavoriteCity).filter(
            FavoriteCity.user_id == user_id,
            FavoriteCity.city_name == city_name
        )
        if existing_city:
            return print('Город уже добавлен в избранное')
        favorite_city = FavoriteCity(
            user_id=user_id,
            city_name=city_name
        )
        db.add(favorite_city)
        db.commit()
        db.refresh(favorite_city)
        return favorite_city


metadata.create_all(engine)
