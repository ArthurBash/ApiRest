from fastapi import FastAPI
from app.db.session import engine
from app.db.base import Base
from app.api.v1 import users
from app.handlers.errors import register_exception_handlers

# Crea las tablas si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Microservicio de Usuarios")

# Incluimos el router
app.include_router(users.router)
register_exception_handlers(app)

