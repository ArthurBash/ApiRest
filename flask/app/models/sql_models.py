from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from flask_sqlalchemy import SQLAlchemy

class User:
    def __init__(self, db):
        self.db = db
        self.Model = db.Model
        self.Column = db.Column
        self.Integer = db.Integer
        self.String = db.String
        self.Boolean = db.Boolean
        self.DateTime = db.DateTime

    def get_model(self):
        class UserModel(self.Model):
            __tablename__ = 'users'

            id = self.Column(self.Integer, primary_key=True)
            username = self.Column(self.String(80), unique=True, nullable=False)
            email = self.Column(self.String(120), unique=True, nullable=False)
            password_hash = self.Column(self.String(128))
            created_at = self.Column(self.DateTime, default=datetime.utcnow)
            updated_at = self.Column(self.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
            is_active = self.Column(self.Boolean, default=True)
            role = self.Column(self.String(20), default='user')

            def set_password(self, password):
                self.password_hash = generate_password_hash(password)

            def check_password(self, password):
                return check_password_hash(self.password_hash, password)

            def generate_token(self, expires_in=3600):
                return create_access_token(identity=self.id, expires_delta=expires_in)

            def as_dict(self):
                return {
                    'id': self.id,
                    'username': self.username,
                    'email': self.email,
                    'created_at': self.created_at.isoformat(),
                    'updated_at': self.updated_at.isoformat(),
                    'is_active': self.is_active,
                    'role': self.role
                }

        return UserModel
