# routes/prediction.py
from flask import Blueprint, jsonify, request
from model.model import predict  # Импорт функции предсказания из model.py

# Создаём Blueprint
prediction_bp = Blueprint('prediction', __name__)

@prediction_bp.route('/predict_yield', methods=['POST'])
def predict_yield():
    """
    Endpoint для предсказания урожайности на основе данных о почве и погоде
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
            soil_type_chernozem:
              type: integer
              example: 1
            soil_type_clay:
              type: integer
              example: 0
            soil_type_loam:
              type: integer
              example: 0
            soil_type_sandy:
              type: integer
              example: 0
    responses:
      200:
        description: Predicted yield
    """
    input_data = request.get_json()
    yield_prediction, mse = predict(input_data)

    return jsonify({
        "predicted_yield": yield_prediction,
        "model_mse": mse
    })
