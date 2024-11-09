# routes/weather.py
import requests
from flask import Blueprint, jsonify, request

# Создаём Blueprint
weather_bp = Blueprint('weather', __name__)

API_KEY = '01aebdb82a1de522e3276a1d5bd32d0b'
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"


@weather_bp.route('/get_weather', methods=['GET'])
def get_weather():
    """
    Endpoint для получения прогноза погоды на основе названия города
    ---
    parameters:
      - name: city
        in: query
        type: string
        required: true
        description: Название города для получения погоды
    responses:
      200:
        description: Прогноз погоды для указанного города
        schema:
          type: object
          properties:
            city:
              type: string
              example: Moscow
            temperature:
              type: number
              example: -3.5
            feels_like:
              type: number
              example: -8.0
            weather_description:
              type: string
              example: Снег
            humidity:
              type: integer
              example: 92
    """
    city = request.args.get('city')
    if not city:
        return jsonify({"error": "City name is required"}), 400

    # Запрос к OpenWeather API
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric',  # используем метрическую систему
        'lang': 'ru'  # язык ответа русский
    }
    response = requests.get(BASE_URL, params=params)

    if response.status_code != 200:
        return jsonify({"error": "Unable to fetch weather data"}), response.status_code

    data = response.json()

    # Извлекаем интересующие нас данные из ответа
    weather_data = {
        "city": city,
        "temperature": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
        "weather_description": data["weather"][0]["description"],
        "humidity": data["main"]["humidity"]
    }

    return jsonify(weather_data)
