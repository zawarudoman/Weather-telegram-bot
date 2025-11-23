from sqlalchemy import Column, Integer, String, DateTime, Boolean, MetaData
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.session import Base, engine, SessionLocal

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
    def create_or_verification(telegram_id: int, username: str, first_name: str, last_name: str):
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


metadata.create_all(engine)

