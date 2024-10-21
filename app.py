from flask import Flask, jsonify, request, redirect
from flasgger import Swagger
import requests

app = Flask(__name__)
swagger = Swagger(app)  # Инициализация Swagger

API_KEY = '01aebdb82a1de522e3276a1d5bd32d0b'

@app.route('/')
def index():
    return redirect('/apidocs/')


@app.route('/weather', methods=['GET'])
def get_weather():
    """
    Get weather data by city
    ---
    parameters:
      - name: city
        in: query
        type: string
        required: true
        description: Name of the city to get the weather data for
    responses:
      200:
        description: Weather recommendations based on the current weather
        schema:
          type: array
          items:
            type: string
      400:
        description: Error fetching weather data
    """
    city = request.args.get('city', default='Moscow', type=str)
    try:
        weather_data = get_weather_data(city)
        recommendations = analyze_weather(weather_data)
        return jsonify(recommendations)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

def get_weather_data(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error fetching weather data: {response.status_code}")

def analyze_weather(data):
    temperature = data['main']['temp']
    weather_condition = data['weather'][0]['description']

    recommendations = []
    if temperature < 10:
        recommendations.append("It is not recommended to plant, the temperature is too low.")
    elif 10 <= temperature < 20:
        recommendations.append("You can plant, but keep an eye on the forecasts.")
    else:
        recommendations.append("Great time for sowing.")

    if 'rain' in weather_condition.lower():
        recommendations.append("Rain is expected, watering is recommended after precipitation.")

    return recommendations

if __name__ == "__main__":
    app.run(debug=True)
