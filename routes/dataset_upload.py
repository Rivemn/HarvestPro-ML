from flask import Blueprint, Flask, request, jsonify
import os
import pandas as pd
from datetime import datetime
from sklearn.preprocessing import StandardScaler

# Blueprint для загрузки датасета
dataset_upload_bp = Blueprint('dataset_upload', __name__)

# Папка для сохранения файлов
DATA_FOLDER = "data/"
MODEL_PATH = "model/risk_model.pkl"

# Инициализируем Swagger
def create_app():
    app = Flask(__name__)
    Swagger(app)  # Инициализация Swagger
    app.register_blueprint(dataset_upload_bp)
    return app

# Хранение информации о загруженных датасетах
uploaded_datasets = {}

def filter_data(data):
    if data.isnull().sum().any():
        data = data.dropna()  # Удалим строки с пропусками

    for col in data.select_dtypes(include=['object']).columns:
        try:
            data[col] = pd.to_numeric(data[col], errors='coerce')
        except Exception as e:
            print(f"Error converting column {col}: {e}")
    
    data = data.dropna()

    if 'risk' in data.columns:
        valid_risks = ["Drought", "Frost", "Flood", "Low Fertility", "Plant Diseases", "No Risk"]
        data = data[data['risk'].isin(valid_risks)]
    
    return data

def determine_data_type(data):
    if 'risk' in data.columns:
        return 'risk'
    elif any(col in data.columns for col in ['yield', 'production', 'harvest']):
        return 'yield'
    return 'unknown'

def process_risk_data(data):
    risk_mapping = {
        "Drought": 0,
        "Frost": 1,
        "Flood": 2,
        "Low Fertility": 3,
        "Plant Diseases": 4,
        "No Risk": 5
    }
    data["risk"] = data["risk"].map(risk_mapping)
    return data

def process_yield_data(data):
    if 'yield' in data.columns:
        scaler = StandardScaler()
        data[['yield']] = scaler.fit_transform(data[['yield']])
    return data

@dataset_upload_bp.route('/upload-dataset', methods=['POST'])
def upload_dataset():
    """
    Endpoint для загрузки CSV файла с уникальным именем.
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
            dataset_name:
              type: string
              example: new_dataset_20231121_123456.csv
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

    # Генерация уникального имени файла с временной меткой
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    dataset_name = f"dataset_{timestamp}.csv"
    file_path = os.path.join(DATA_FOLDER, dataset_name)

    # Сохраняем файл
    os.makedirs(DATA_FOLDER, exist_ok=True)  # Создаем папку, если ее нет
    file.save(file_path)

    # Загружаем новый датасет
    try:
        data = pd.read_csv(file_path)
    except Exception as e:
        return jsonify({"error": f"Failed to read the dataset: {str(e)}"}), 400

    # Фильтрация данных
    data = filter_data(data)  # Фильтруем данные
    data_type = determine_data_type(data)  # Определяем тип данных

    # Обработка данных в зависимости от типа
    if data_type == 'risk':
        data = process_risk_data(data)  # Обрабатываем для рисков
    elif data_type == 'yield':
        data = process_yield_data(data)  # Обрабатываем для урожайности

    # Сохраняем информацию о датасете
    dataset_info = {
        "columns": data.columns.tolist(),
        "num_rows": len(data),
        "num_columns": len(data.columns)
    }
    uploaded_datasets[dataset_name] = dataset_info

    return jsonify({
        "message": "Dataset uploaded successfully",
        "dataset_name": dataset_name,
        "dataset_info": dataset_info
    })
