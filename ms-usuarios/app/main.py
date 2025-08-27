# app/main.py
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.users import router as users
from app.api.v1.inicial import router as inicial_router 
from app.handlers.errors import register_user_exception_handlers
from app.middleware.rate_limit import RateLimitMiddleware
from app.db.base import  Base
from app.db.session import engine

from fastapi.openapi.utils import get_openapi


app = FastAPI(
    title="Microservicio de manejo de Usuarios",
    description="Microservicio para gestión de usuarios con autenticación JWT",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="Microservicio de manejo de Usuarios",
        version="1.0.0",
        description="Microservicio para gestión de usuarios con autenticación JWT",
        routes=app.routes,
    )
    
    openapi_schema["components"]["securitySchemes"] = {
    "OAuth2PasswordBearer": {
        "type": "oauth2",
        "flows": {
            "password": {
                "tokenUrl": "/api/v1/users/token/login",
                "scopes": {}
            }
        }
    }
}
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Middleware de Rate Limiting
app.add_middleware(
    RateLimitMiddleware,
    calls=5,
    period=60
)

# Middleware de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar routers importados
app.include_router(users)
app.include_router(inicial_router, prefix="/api/v1/inicial")

# Registrar manejadores de excepciones
register_user_exception_handlers(app)

# Crear tablas al arrancar (solo en startup)
@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)
