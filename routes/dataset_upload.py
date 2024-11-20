from flask import Blueprint, Flask, request, jsonify
import os
import pandas as pd
import joblib
from flasgger import Swagger

# Blueprint для загрузки датасета
dataset_upload_bp = Blueprint('dataset_upload', __name__)

# Путь для сохранения файлов
DATASET_PATH = "data/new_dataset.csv"
MODEL_PATH = "model/risk_model.pkl"

# Инициализируем Swagger
def create_app():
    app = Flask(__name__)
    Swagger(app)  # Инициализация Swagger
    app.register_blueprint(dataset_upload_bp)
    return app

@dataset_upload_bp.route('/upload-dataset', methods=['POST'])
def upload_dataset():
    """
    Endpoint для загрузки CSV файла.
    ---
    parameters:
      - name: file
        in: formData
        type: file
        required: true
        description: Загружаемый CSV файл с данными
    responses:
      200:
        description: Успешная загрузка датасета
        schema:
          type: object
          properties:
            message:
              type: string
              example: Dataset uploaded successfully
            dataset_info:
              type: object
              properties:
                columns:
                  type: array
                  items:
                    type: string
                num_rows:
                  type: integer
                num_columns:
                  type: integer
      400:
        description: Ошибка при загрузке файла
        schema:
          type: object
          properties:
            error:
              type: string
              example: No file part
    """
    # Проверка наличия файла в запросе
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Сохраняем файл
    os.makedirs("data", exist_ok=True)  # Создаем папку data, если ее нет
    file.save(DATASET_PATH)

    # Загружаем новый датасет
    try:
        data = pd.read_csv(DATASET_PATH)
    except Exception as e:
        return jsonify({"error": f"Failed to read the dataset: {str(e)}"}), 400

    # Отправляем сообщение с основными сведениями о датасете
    dataset_info = {
        "columns": data.columns.tolist(),
        "num_rows": len(data),
        "num_columns": len(data.columns)
    }

    return jsonify({
        "message": "Dataset uploaded successfully",
        "dataset_info": dataset_info
    })
