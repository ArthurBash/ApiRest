from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
import os

# Inicializar extensiones sin aplicación
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    
    # Inicializar extensiones con la app
    db.init_app(app)
    migrate.init_app(app, db) 
    bcrypt.init_app(app)
    
    # Registrar blueprints
    from app.routes.api_routes import user_bp
    app.register_blueprint(user_bp, url_prefix='/api')
    
    # Importar modelos para que Flask-Migrate los detecte
    with app.app_context():
        from app.models import user
    
    return app