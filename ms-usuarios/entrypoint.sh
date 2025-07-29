#!/bin/bash
set -e  # salir si algún comando falla

echo "Ejecutando script de inicialización..."
python init_db.py

echo "Iniciando servidor Uvicorn..."
exec uvicorn app.main:app --host 0.0.0.0 --port 80 --reload

# TODO fijarse como hacer para hacer solo roload cuando esta en development 
# TODO fijarse de agrega rla creacion de un  env.secret_key por uno fuerte y seguro. random

