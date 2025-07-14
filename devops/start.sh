#!/bin/bash

# Inicializar migraciones solo si no existen
if [ ! -d "/app/migrations/versions" ]; then
    echo "Inicializando migraciones de base de datos..."
    flask db init --directory /app/migrations
fi

# Aplicar migraciones
echo "Aplicando migraciones de base de datos..."
flask db upgrade --directory /app/migrations


# Determinar el entorno (development/production)
if [ "$FLASK_ENV" = "development" ]; then
    echo "Entorno de desarrollo detectado, iniciando servidor de desarrollo..."
    exec flask run --host=0.0.0.0 --port=5000
else
    echo "Entorno de producción detectado, iniciando Gunicorn..."
    # Puedes ajustar el número de workers según los cores de tu CPU
    exec gunicorn -w $WORKERS -b 0.0.0.0:5000 "app:create_app()"
fi