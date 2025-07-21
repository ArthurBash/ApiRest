from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from pymongo import MongoClient

db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()

def get_mongo_client(mongo_uri):
    """Devuelve una instancia de MongoClient configurada"""
    return MongoClient(mongo_uri)
