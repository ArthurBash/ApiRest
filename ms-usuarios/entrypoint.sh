#!/bin/bash
set -e


# echo "Creando nueva migracion..."
# alembic revision --autogenerate -m "Añadir tabla de Usuarios"

echo "Aplicando las migraciones..."
alembic upgrade head

echo "Esperando aplicaciones... ...."
sleep 5

echo "Ejecutando script de inicialización..."
python init_db.py

echo "Iniciando servidor Uvicorn..."
if [ "$ENVIRONMENT" = "development" ]; then
    exec uvicorn app.main:app --host 0.0.0.0 --port 80 --reload
else
    exec uvicorn app.main:app --host 0.0.0.0 --port 80
fi
