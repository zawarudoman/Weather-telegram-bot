import requests
import config


class WeatherService:
    def __init__(self):
        self.api_key = config.WEATHER_API_KEY
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"

    def get_weather(self, city):
        try:
            params = {
                'q': city,
                'appid': self.api_key,
                'units': 'metric',  # для градусов Цельсия
                'lang': 'ru'
            }

            response = requests.get(self.base_url, params=params)
            data = response.json()

            if response.status_code == 200:
                return self._format_weather(data)
            else:
                return f"Ошибка: {data.get('message', 'Город не найден')}"

        except Exception as e:
            return f"Произошла ошибка: {str(e)}"

    def _format_weather(self, data):
        city = data['name']
        country = data['sys']['country']
        temp = round(data['main']['temp'])
        feels_like = round(data['main']['feels_like'])
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        description = data['weather'][0]['description'].capitalize()
        wind_speed = data['wind']['speed']

        weather_text = (
            f"🌍 {city}, {country}\n"
            f"🌡️ Температура: {temp}°C (ощущается как {feels_like}°C)\n"
            f"📝 {description}\n"
            f"💧 Влажность: {humidity}%\n"
            f"🎯 Давление: {pressure} гПа\n"
            f"💨 Ветер: {wind_speed} м/с"
        )

        return weather_text
