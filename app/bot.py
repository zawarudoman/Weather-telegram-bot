from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import config
from weather_api import WeatherService
from app.models.user import User
from app.models.user_manager import UserManager


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

        📍 Примеры:
        Москва
        London
        Paris

        ❓ Помощь: /help
        """
        update.message.reply_text(welcome_text)
        data_user = update.message['chat']
        UserManager.create_or_update_user(
            data_user['id'],
            data_user['username'],
            data_user['first_name'],
            data_user['last_name']
        )

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

    def handle_message(self, update):
        city = update.message.text.strip()
        self.send_weather(update, city)

    def send_weather(self, update, city: str):
        weather_info = self.weather_service.get_weather(city)
        update.message.reply_text(weather_info)


if __name__ == "__main__":
    bot = WeatherBot()
    bot.start()
