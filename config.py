# config.py
import os

from urllib.parse import quote_plus

class Config:
    #password = quote_plus("COvTgfBJLPCwbT3QqHsqW56NkHuywoLX")
    SQLALCHEMY_DATABASE_URI = r'postgresql://api_ouo8_user:COvTgfBJLPCwbT3QqHsqW56NkHuywoLX@dpg-cs6llntsvqrc73f5vq3g-a.oregon-postgres.render.com/api_ouo8'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Clé secrète pour les sessions et JWT
    SECRET_KEY = os.getenv("SECRET_KEY", "mysecretkey")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwtsecret")
