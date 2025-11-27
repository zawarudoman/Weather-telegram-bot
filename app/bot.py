from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import config
from app.models.user import User
from app.models.favorite_city import FavoriteCity
from weather_api import WeatherService
from app.database.session import create_tables, SessionLocal


def init_database():
    """Инициализация базы данных"""
    print("Создание таблиц...")
    create_tables()
    print("Таблицы созданы успешно!")


class WeatherBot:
    def __init__(self):
        self.token = config.TELEGRAM_TOKEN
        self.weather_service = WeatherService()
        self.updater = Updater(token=self.token, use_context=True)
        self.dispatcher = self.updater.dispatcher

    def setup_handlers(self):
        self.dispatcher.add_handler(CommandHandler("start", self.start_command))
        self.dispatcher.add_handler(CommandHandler("help", self.help_command))
        self.dispatcher.add_handler(CommandHandler("weather", self.weather_command))
        self.dispatcher.add_handler(CommandHandler("favorite", self.favorite_command))
        self.dispatcher.add_handler(CommandHandler("favorite_city", self.add_favorite_command))
        self.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, self.handle_message))


    def start(self):
        self.setup_handlers()
        print("Бот запущен...")
        self.updater.start_polling()
        self.updater.idle()

    def start_command(self, update, context):
        welcome_text = """
        👋 Привет! Я погодный бот.

        🌤️ Чтобы узнать погоду, отправь мне:
        - Название города
        - Или используй команду /weather Москва
        
        🏙️ Добавить любимый город:
        - Используй команду /favorite_city
        - Узнать свои любимые города /favorite
        
        📍 Примеры:
        Москва
        London
        Paris

        ❓ Помощь: /help
        """
        update.message.reply_text(welcome_text)
        data_user = update.message['chat']
        User.get_or_create(
            data_user['id'],
            data_user['username'],
            data_user['first_name'],
            data_user['last_name']
        )
        print(f'Создана запись в таблице User {data_user["username"]}')

    def help_command(self, update):
        help_text = """
        📖 Доступные команды:

        /start - начать работу
        /help - эта справка
        /weather [город] - узнать погоду

        🌍 Просто отправь название города, и я покажу погоду!
        """
        update.message.reply_text(help_text)

    def weather_command(self, update, context):
        if not context.args:
            update.message.reply_text("⚠️ Укажите город: /weather Москва")
            return

        city = ' '.join(context.args)
        self.send_weather(update, city)

    def favorite_command(self, update, context):
        favorite_city_text = """
        У тебя пока нет любимых городов(
        
        Давай добавим их, напиши мне /favorite_city Москва
        И я добавлю этот город в список твоих любимых
        """
        get_user_id = update.message.chat_id
        city = User.get_favorite_cities(get_user_id)
        if city is not None:
            update.message.reply_text(f'Твои любимые города: {city}')
        else:
            update.message.reply_text(favorite_city_text)

    def add_favorite_command(self, update, context):
        text = """
        Добавил город в твои любимые
        """
        city_name = ' '.join(context.args)
        get_user_id = int(update.message.chat_id)
        User.add_favorite_city(get_user_id, city_name)

    def handle_message(self, update, context):
        city = update.message.text.strip()
        self.send_weather(update, city)

    def send_weather(self, update, city: str):
        weather_info = self.weather_service.get_weather(city)
        update.message.reply_text(weather_info)


if __name__ == "__main__":
    init_database()
    bot = WeatherBot()
    bot.start()
