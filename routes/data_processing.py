from flask import Blueprint, request, jsonify
import os
import pandas as pd
import joblib

# Blueprint для загрузки датасета
dataset_upload_bp = Blueprint('dataset_upload', __name__)

# Путь для сохранения файлов
DATASET_PATH = "data/new_dataset.csv"
MODEL_PATH = "model/risk_model.pkl"

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
        from sklearn.preprocessing import StandardScaler
        scaler = StandardScaler()
        data[['yield']] = scaler.fit_transform(data[['yield']])
    return data

@dataset_upload_bp.route('/upload-dataset', methods=['POST'])
def upload_dataset():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    os.makedirs("data", exist_ok=True)
    file.save(DATASET_PATH)

    try:
        data = pd.read_csv(DATASET_PATH)
    except Exception as e:
        return jsonify({"error": f"Failed to read the dataset: {str(e)}"}), 400

    data = filter_data(data)  # Фильтруем данные
    data_type = determine_data_type(data)  # Определяем тип данных

    if data_type == 'risk':
        data = process_risk_data(data)  # Обрабатываем для рисков
    elif data_type == 'yield':
        data = process_yield_data(data)  # Обрабатываем для урожайности

    return jsonify({
        "message": f"Dataset uploaded and processed as {data_type}",
        "dataset_info": {
            "columns": data.columns.tolist(),
            "num_rows": len(data),
            "num_columns": len(data.columns)
        }
    })
