import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# Загрузка датасета
data = pd.read_csv("risk_data.csv")

# Преобразование текстовых рисков в числовые
risk_mapping = {
    "Drought": 0,
    "Frost": 1,
    "Flood": 2,
    "Low Fertility": 3,
    "Plant Diseases": 4,
    "No Risk": 5
}
data["risk"] = data["risk"].map(risk_mapping)

# Выделение признаков и метки
X = data.drop("risk", axis=1)
y = data["risk"]

# Разделение данных на тренировочную и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Обучение модели
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Оценка модели
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# Сохранение модели
import joblib
joblib.dump(model, "risk_model.pkl")
print("Модель сохранена как risk_model.pkl")
