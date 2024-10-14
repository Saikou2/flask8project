from app import create_app
from flask_swagger_ui import get_swaggerui_blueprint
import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# Créer l'application Flask
app = create_app()

# Configuration de Swagger
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'  # Chemin vers votre fichier swagger.json

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Mon API"
    }
)

# Enregistrer le blueprint Swagger
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)