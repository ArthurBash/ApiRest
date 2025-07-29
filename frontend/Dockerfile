FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiamos requirements y lo instalamos
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Crear usuario no root
RUN addgroup --system flask && adduser --system --ingroup flask --uid 1000 flask

# Copiar toda la carpeta del proyecto frontend (app, manage.py, etc)
COPY . .

USER flask

EXPOSE 5000

CMD ["python", "-m", "app.main"]
