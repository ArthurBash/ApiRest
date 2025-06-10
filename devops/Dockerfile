# Imagen base oficial
FROM python:3.11-slim

# Crear directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        bash \
        dos2unix \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependencias de Python
COPY ./devops/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Crear usuario no root
RUN addgroup --system flask \
    && adduser --system --ingroup flask --uid 1000 flask

# Copiar el código fuente
COPY ../app /app/app
COPY ./devops/config.py /app/config.py
COPY ./start.sh /app/start.sh

# Convertir finales de línea y dar permisos
RUN sed -i 's/\r$//g' /app/start.sh \
    && chmod +x /app/start.sh \
    && chmod +x /app/app/__init__.py

# Configurar usuario y permisos
RUN chown -R flask:flask /app
USER flask

# Exponer puerto
EXPOSE 5000

# Comando de inicio
CMD ["bash", "-c", "/app/start.sh"]
