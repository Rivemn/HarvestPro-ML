from flask import Blueprint, request, jsonify
import os
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, classification_report, mean_squared_error, r2_score

# Путь для сохранения файлов
DATASET_PATH = "data/new_dataset.csv"
MODEL_PATH = "model/risk_model.pkl"

dataset_upload_bp = Blueprint('dataset_upload', __name__)

def filter_data(data):
    if data.isnull().sum().any():
        data = data.dropna()

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

def prepare_data(data, target_column):
    X = data.drop(columns=[target_column])
    y = data[target_column]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test

def train_classification_model(X_train, y_train):
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    return model

def train_regression_model(X_train, y_train):
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    return model

def evaluate_classification_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    return accuracy, report

def evaluate_regression_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    return mse, r2

def save_model(model, model_path):
    joblib.dump(model, model_path)

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

    data = filter_data(data)
    data_type = determine_data_type(data)

    if data_type == 'risk':
        X_train, X_test, y_train, y_test = prepare_data(data, 'risk')
        model = train_classification_model(X_train, y_train)
        accuracy, report = evaluate_classification_model(model, X_test, y_test)
    elif data_type == 'yield':
        X_train, X_test, y_train, y_test = prepare_data(data, 'yield')
        model = train_regression_model(X_train, y_train)
        mse, r2 = evaluate_regression_model(model, X_test, y_test)
    
    save_model(model, MODEL_PATH)

    return jsonify({
        "message": f"Model trained and saved as {data_type}",
        "evaluation": {
            "accuracy": accuracy if data_type == 'risk' else None,
            "report": report if data_type == 'risk' else None,
            "mse": mse if data_type == 'yield' else None,
            "r2": r2 if data_type == 'yield' else None
        }
    })
