import os

class Config:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://edufuengirola1:rootroot@edufuengirola1.mysql.eu.pythonanywhere-services.com/edufuengirola1$la_nueva_era_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'clave_secreta'
    JWT_ACCESS_TOKEN_EXPIRES = int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES', 3600)) # Expiración en segundos (3600s - 1h)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'clave_secreta'