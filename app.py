from flask import Flask, jsonify, request
from flasgger import Swagger
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

app = Flask(__name__)
swagger = Swagger(app)

# Загрузка и предобработка данных
data = pd.read_csv("fields_data.csv")
# Создание дамми-переменных для всех типов почвы
data = pd.get_dummies(data, columns=['soil_type'], drop_first=True)

# Разделение данных на признаки и целевую переменную
X = data.drop('yield', axis=1)
y = data['yield']

# Разделение на тренировочные и тестовые данные
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Инициализация и обучение модели
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Оценка модели на тестовой выборке
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)

@app.route('/predict_yield', methods=['POST'])
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
              example: 1  # 1 если чернозем, 0 иначе
            soil_type_clay:
              type: integer
              example: 0  # 1 если глинистая почва, 0 иначе
            soil_type_loam:
              type: integer
              example: 0  # 1 если суглинок, 0 иначе
            soil_type_sandy:
              type: integer
              example: 0  # 1 если песчаная почва, 0 иначе
    responses:
      200:
        description: Predicted yield
    """
    # Получение входных данных
    input_data = request.get_json()

    # Приведение входных данных к DataFrame
    input_df = pd.DataFrame([input_data])

    # Убедитесь, что все необходимые столбцы присутствуют
    for col in X.columns:
        if col not in input_df.columns:
            input_df[col] = 0  # Добавьте недостающие столбцы с нулевым значением

    # Предсказание урожайности
    yield_prediction = model.predict(input_df[X.columns])[0]

    return jsonify({
        "predicted_yield": yield_prediction,
        "model_mse": mse
    })


if __name__ == '__main__':
    app.run(debug=True)
