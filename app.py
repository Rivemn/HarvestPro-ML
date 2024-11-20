from flask import Flask
from flasgger import Swagger
from routes import blueprints  # Импортируем все blueprints из routes

app = Flask(__name__)
swagger = Swagger(app)

# Регистрируем все blueprints
for blueprint in blueprints:
    app.register_blueprint(blueprint)

if __name__ == '__main__':
    app.run(debug=True)
