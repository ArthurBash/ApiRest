FROM python:3.9-slim

WORKDIR /app

COPY ./devops/requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p app

# Crear usuario no root
RUN addgroup --system flask \
&& adduser --system --ingroup flask --uid 1000 flask

COPY ../app /app/app

EXPOSE 5000

USER flask

CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5000"]
