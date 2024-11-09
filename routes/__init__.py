# routes/__init__.py
from .prediction import prediction_bp
from .weather import weather_bp
from .recommendations import recommendations_bp  # Импортируем новый маршрут рекомендаций

blueprints = [prediction_bp, weather_bp, recommendations_bp]
