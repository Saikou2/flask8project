# config.py
import os

class Config:
    # URI de la base de données (utilisation d'une base SQLite pour les tests)
   SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', 'postgresql://api_ouo8_user:COvTgfBJLPCwbT3QqHsqW56NkHuywoLX@dpg-cs6llntsvqrc73f5vq3g-a/api_ouo8')
   SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Clé secrète pour les sessions et JWT
   SECRET_KEY = os.getenv("SECRET_KEY", "mysecretkey")
   JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwtsecret")
