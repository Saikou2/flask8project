from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flasgger import Swagger
from flask_cors import CORS 
from config import Config 


# Initialisation des extensions
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)  
    # Initialisation des extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Initialisation de Flasgger pour Swagger UI
    swagger = Swagger(app)

    # Configurer CORS pour autoriser toutes les origines
    CORS(app)

    # Enregistrement des Blueprints
    from app.routes import main  # Vérifiez que 'main' est le nom correct
    from app.auth import auth  # Assurez-vous que 'auth' est correct
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(main, url_prefix='/api')  # Enregistrement du blueprint principal
      # Enregistrement du blueprint d'authentification

    return app
