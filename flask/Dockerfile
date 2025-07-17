FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY ./devops/requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p app

# Crear usuario no root
RUN addgroup --system flask \
&& adduser --system --ingroup flask --uid 1000 flask

COPY ../app /app/app

COPY devops/start.sh start.sh
RUN chmod +x start.sh && sed -i 's/\r$//g' start.sh

COPY --chown=flask:flask ./app/migrations ./app/migrations

EXPOSE 5000

USER flask

CMD ["./start.sh"]