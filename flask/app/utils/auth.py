# app/utils/auth.py

from flask_jwt_extended import create_access_token, get_jwt_identity, verify_jwt_in_request
from functools import wraps
from app.services.user_service import UserService
from flask import request, current_app

class AuthUtils:
    def __init__(self, app=None):
        self.app = app
        self.user_service = None
        if app:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        self.user_service = UserService(app)

    def generate_token(self, user_data):
        """Generar un token JWT para el usuario"""
        if not self.app:
            raise RuntimeError("AuthUtils no ha sido inicializado con una aplicación")
        with self.app.app_context():
            return create_access_token(identity=user_data['username'])

    def verify_token(self, token):
        """Verificar un token JWT"""
        if not self.app:
            raise RuntimeError("AuthUtils no ha sido inicializado con una aplicación")
        with self.app.app_context():
            try:
                verify_jwt_in_request()
                return True
            except:
                return False

    def get_current_user(self):
        """Obtener el usuario actual desde el token"""
        if not self.app:
            raise RuntimeError("AuthUtils no ha sido inicializado con una aplicación")
        with self.app.app_context():
            current_user = get_jwt_identity()
            if current_user:
                return self.user_service.get_user_by_username(current_user)[0]
            return None

def jwt_required(fn):
    """Decorador para endpoints que requieren autenticación"""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        auth_utils = AuthUtils()
        if not auth_utils.verify_token(request.headers.get('Authorization')):
            return {'error': 'Token inválido o expirado'}, 401
        return fn(*args, **kwargs)
    return wrapper

def admin_required(fn):
    """Decorador para endpoints que requieren privilegios de administrador"""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        auth_utils = AuthUtils()
        current_user = auth_utils.get_current_user()
        if not current_user or current_user.get('role') != 'admin':
            return {'error': 'Acceso no autorizado'}, 403
        return fn(*args, **kwargs)
    return wrapper
    expires = timedelta(hours=1)
    access_token = create_access_token(identity=identity, expires_delta=expires)
    return access_token
