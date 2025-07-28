from flask import Flask
import os


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

    # Importar rutas y registrar blueprint
    from .routes.api_routes import main
    app.register_blueprint(main)

    return app
