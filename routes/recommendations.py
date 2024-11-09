# routes/recommendations.py
from flask import Blueprint, jsonify, request

recommendations_bp = Blueprint('recommendations', __name__)


@recommendations_bp.route('/get_recommendations', methods=['POST'])
def get_recommendations():
    """
    Endpoint для получения рекомендаций по посадке на основе данных о почве и погоде
    ---
    parameters:
      - name: input_data
        in: body
        required: true
        schema:
          type: object
          properties:
            ph_level:
              type: number
              example: 6.5
            n_content:
              type: number
              example: 2.3
            p_content:
              type: number
              example: 1.7
            k_content:
              type: number
              example: 2.1
            temperature:
              type: number
              example: 23
            rainfall:
              type: number
              example: 90
            humidity:
              type: number
              example: 55
            soil_type:
              type: string
              example: "chernozem"
    responses:
      200:
        description: Рекомендации для улучшения условий посадки
    """
    input_data = request.get_json()

    ph_level = input_data.get('ph_level')
    n_content = input_data.get('n_content')
    p_content = input_data.get('p_content')
    k_content = input_data.get('k_content')
    temperature = input_data.get('temperature')
    rainfall = input_data.get('rainfall')
    humidity = input_data.get('humidity')
    soil_type = input_data.get('soil_type')

    # Анализ по типу почвы
    soil_recommendations = {
        "chernozem": "Чернозем идеально подходит для выращивания зерновых культур.",
        "clay": "Глинистая почва хорошо подходит для посадки винограда и деревьев, но требует улучшения дренажа.",
        "loam": "Суглинок универсален и подходит для большинства культур.",
        "sandy": "Песчаная почва быстро теряет влагу. Рекомендуется частый полив и добавление органических удобрений."
    }

    # Рекомендация по содержанию pH
    if ph_level < 5.5:
        ph_recommendation = "Рекомендуется поднять уровень pH добавлением извести."
    elif ph_level > 7.5:
        ph_recommendation = "Рекомендуется понизить уровень pH добавлением серы."
    else:
        ph_recommendation = "Уровень pH подходит для большинства культур."

    # Рекомендации по удобрениям
    fertilizer_recommendations = []
    if n_content < 1.5:
        fertilizer_recommendations.append("Добавьте азотные удобрения для улучшения роста.")
    if p_content < 1.0:
        fertilizer_recommendations.append("Добавьте фосфорные удобрения для развития корневой системы.")
    if k_content < 1.5:
        fertilizer_recommendations.append("Добавьте калийные удобрения для устойчивости к болезням.")

    # Рекомендация по температуре и влажности
    if temperature < 10:
        temp_recommendation = "Температура слишком низкая для посадки, рекомендуется подождать потепления."
    elif temperature > 30:
        temp_recommendation = "Температура слишком высокая для посадки, следите за уровнем влажности."
    else:
        temp_recommendation = "Температура благоприятная для посадки."

    if rainfall < 50:
        water_recommendation = "Необходим дополнительный полив, так как уровень осадков низкий."
    elif rainfall > 150:
        water_recommendation = "Рекомендуется дренаж, так как уровень осадков высокий."
    else:
        water_recommendation = "Уровень осадков в норме."

    # Составляем рекомендации
    recommendations = {
        "soil_type_recommendation": soil_recommendations.get(soil_type, "Нет рекомендаций для данного типа почвы."),
        "ph_recommendation": ph_recommendation,
        "fertilizer_recommendations": fertilizer_recommendations,
        "temperature_recommendation": temp_recommendation,
        "water_recommendation": water_recommendation,
        "humidity_level": humidity
    }

    return jsonify(recommendations)
