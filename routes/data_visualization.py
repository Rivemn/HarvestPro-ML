from flask import Blueprint, jsonify, request, send_file
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO

# Blueprint для визуализации данных
data_visualization_bp = Blueprint('data_visualization', __name__)

DATA_FOLDER = "data/"  # Путь к папке с загруженными данными

@data_visualization_bp.route('/visualize', methods=['GET'])
def visualize_data():
    """
    Endpoint для визуализации данных из загруженного датасета.
    ---
    parameters:
      - name: dataset_name
        in: query
        type: string
        required: true
        description: Имя датасета для визуализации
    responses:
      200:
        description: Визуализация данных в виде графика
        content:
          image/png:
            schema:
              type: string
              format: binary
      400:
        description: Ошибка при визуализации данных
        schema:
          type: object
          properties:
            error:
              type: string
              example: Dataset not found
    """
    # Получаем имя датасета из параметров запроса
    dataset_name = request.args.get('dataset_name')
    if not dataset_name:
        return jsonify({"error": "Dataset name is required"}), 400

    file_path = os.path.join(DATA_FOLDER, dataset_name)
    
    # Проверка наличия файла
    if not os.path.exists(file_path):
        return jsonify({"error": "Dataset not found"}), 400

    # Загружаем данные
    try:
        data = pd.read_csv(file_path)
    except Exception as e:
        return jsonify({"error": f"Failed to load dataset: {str(e)}"}), 400

    # Преобразование текстовых значений в числовые (если это необходимо)
    if 'risk' in data.columns:
        risk_mapping = {
            "Drought": 0,
            "Frost": 1,
            "Flood": 2,
            "Low Fertility": 3,
            "Plant Diseases": 4,
            "No Risk": 5
        }
        data['risk'] = data['risk'].map(risk_mapping)  # Преобразование текстов в числа

    # Фильтрация только числовых столбцов для корреляции
    numeric_data = data.select_dtypes(include=['number'])

    if numeric_data.empty:
        return jsonify({"error": "No numeric data available for correlation"}), 400

    # Генерация визуализации (пример — корреляционная матрица)
    plt.figure(figsize=(10, 8))
    sns.heatmap(numeric_data.corr(), annot=True, cmap="coolwarm", linewidths=0.5)
    plt.title("Корреляционная матрица")

    # Сохранение графика в буфер
    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close()

    return send_file(buf, mimetype='image/png', as_attachment=False, download_name="visualization.png")
