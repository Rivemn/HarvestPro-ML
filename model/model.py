# model/model.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

# Загрузка и предобработка данных
data = pd.read_csv("fields_data.csv")
data = pd.get_dummies(data, columns=['soil_type'], drop_first=True)

# Разделение данных на признаки и целевую переменную
X = data.drop('yield', axis=1)
y = data['yield']

# Разделение на тренировочные и тестовые данные
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Инициализация и обучение модели
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Оценка модели
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)

def predict(input_data):
    """Функция предсказания урожайности"""
    # Преобразуем входные данные в DataFrame
    input_df = pd.DataFrame([input_data])
    for col in X.columns:
        if col not in input_df.columns:
            input_df[col] = 0

    # Предсказываем урожайность
    return model.predict(input_df[X.columns])[0], mse
