# app/main.py

from fastapi import FastAPI
from app.db.session import engine
from app.db.base import Base
from app.api.v1 import photos,folders

app = FastAPI(title="Microservicio de fotos")

# Creamos esquema al arrancar la aplicación (solo en el proceso que sirve peticiones)
@app.on_event("startup")
def create_schema():
    Base.metadata.create_all(bind=engine)

# Incluimos el router
app.include_router(photos.router)
app.include_router(folders.router)
# register_exception_handlers(app)  # si vuelves a habilitar tus handlers
