from flasgger import Swagger, swag_from
from flask import Blueprint, request, jsonify
import joblib
import numpy as np

risk_assessment_bp = Blueprint('risk_assessment', __name__)

# Загрузка модели
model = joblib.load("risk_model.pkl")

@risk_assessment_bp.route('/risk-assessment', methods=['POST'])
@swag_from({
    'summary': 'Оценка риска для урожая',
    'description': 'Этот эндпоинт оценивает возможные риски для урожая на основе переданных данных (погода, почва и т.д.).',
    'parameters': [
        {
            'name': 'data',
            'in': 'body',
            'type': 'object',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'temperature': {'type': 'number', 'example': 30},
                    'rainfall': {'type': 'number', 'example': 100},
                    'humidity': {'type': 'number', 'example': 60},
                    'wind_speed': {'type': 'number', 'example': 5},
                    'soil_ph': {'type': 'number', 'example': 6.5},
                    'soil_moisture': {'type': 'number', 'example': 50},
                    'soil_density': {'type': 'number', 'example': 1.3},
                    'light_hours': {'type': 'number', 'example': 12}
                }
            }
        }
    ],
    'responses': {
        '200': {
            'description': 'Риск успешно рассчитан',
            'schema': {
                'type': 'object',
                'properties': {
                    'risk': {'type': 'string', 'example': 'Drought'}
                }
            }
        },
        '400': {
            'description': 'Неверные данные'
        }
    }
})
def risk_assessment():
    # Получение данных от клиента
    data = request.json
    features = np.array([[
        data["temperature"],
        data["rainfall"],
        data["humidity"],
        data["wind_speed"],
        data["soil_ph"],
        data["soil_moisture"],
        data["soil_density"],
        data["light_hours"]
    ]])

    # Предсказание риска
    risk_pred = model.predict(features)[0]

    # Преобразование предсказания в текст
    risk_mapping = {
        0: "Drought",
        1: "Frost",
        2: "Flood",
        3: "Low Fertility",
        4: "Plant Diseases",
        5: "No Risk"
    }
    risk_name = risk_mapping[risk_pred]

    return jsonify({"risk": risk_name})
