
FROM python:3.11


WORKDIR /code


COPY requirements.txt /code/requirements.txt


RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt


COPY app /code/app
COPY ./alembic.ini /code/alembic.ini
COPY ./alembic /code/alembic
COPY entrypoint.sh /code/entrypoint.sh
RUN chmod +x /code/entrypoint.sh

COPY init_db.py /code/init_db.py
RUN chmod +x /code/init_db.py
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]

ENTRYPOINT ["/code/entrypoint.sh"]

