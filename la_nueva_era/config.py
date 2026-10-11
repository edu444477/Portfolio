import os
from urllib.parse import urlparse


class Config:
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES', 3600))
    SECRET_KEY = os.environ.get('SECRET_KEY')

    # PostgreSQL (Neon) con schema 'tfg'
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        # Asegurar channel_binding=require para Neon
        if 'channel_binding' not in database_url:
            separator = '&' if '?' in database_url else '?'
            database_url += f'{separator}channel_binding=require'
        # Forzar search_path al schema tfg
        if 'options=' not in database_url:
            separator = '&' if '?' in database_url else '?'
            database_url += f'{separator}options=-csearch_path%3Dtfg'
    SQLALCHEMY_DATABASE_URI = database_url or "postgresql://localhost/tfg"

    # CORS
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', 'http://localhost:5173').split(',')

    # Redis (Upstash)
    REDIS_URL = os.environ.get('REDIS_URL')

    # Configuración de migraciones
    SQLALCHEMY_ECHO = os.environ.get('SQLALCHEMY_ECHO', 'False').lower() == 'true'