import pytest

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app


@pytest.fixture
def app():
    os.environ["FLASK_ENV"] = "dev"
    app = create_app()
    return app

def test_mongo_connection(app):
    with app.app_context():
        mongo_client = getattr(app, "mongo_client", None)
        assert mongo_client is not None, "Mongo client should be initialized in dev environment"

        # Probar acceso a la base de datos
        test_db = mongo_client.test_db
        test_col = test_db.test_collection

        result = test_col.insert_one({"test_key": "test_value"})
        assert result.acknowledged is True

        fetched = test_col.find_one({"test_key": "test_value"})
        assert fetched is not None
        assert fetched["test_key"] == "test_value"

        # Limpiar
        test_col.delete_many({})
