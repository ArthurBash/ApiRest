#!/usr/bin/env python
import os
from flask_migrate import Migrate
from app import create_app, db
from app.models.user import User  

app = create_app()

# Inicializar Flask-Migrate
migrate = Migrate(app, db)

# Contexto para shell (para trabajar con modelos en CLI)
@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)