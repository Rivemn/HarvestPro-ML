from .prediction import prediction_bp
from .weather import weather_bp
from .recommendations import recommendations_bp  
from .risk_assessment import risk_assessment_bp
from .dataset_upload import dataset_upload_bp
from .data_visualization import data_visualization_bp  # Импортируем Blueprint для визуализации


blueprints = [prediction_bp, weather_bp, recommendations_bp, risk_assessment_bp,dataset_upload_bp,data_visualization_bp]
