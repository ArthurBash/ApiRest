# 📸 Galería de Imágenes - Flask + FastAPI + Microservicios + MinIO + PostgreSQL

Proyecto de arquitectura moderna basado en microservicios, desarrollado con **Flask (Frontend)** y **FastAPI (Backend)**. Permite a los usuarios registrarse, iniciar sesión, subir imágenes, organizarlas en carpetas, filtrarlas por tags, nombre o fecha, y definir si son públicas o privadas.  
Todas las fotos son almacenadas en **MinIO (S3 compatible)**. La seguridad está implementada mediante **JWT**, contraseñas hasheadas y control de permisos.

---

## 🏛️ Arquitectura General

Frontend (Flask)
│
├──> Microservicio Usuarios (FastAPI + PostgreSQL) [JWT / Hash Passwords]
├──> Microservicio Fotos (FastAPI + PostgreSQL + MinIO S3)
└──> Microservicio Carpetas (FastAPI + MongoDB)


---

## 🚀 Cómo levantar el proyecto completo (Docker Compose)
Este proyecto incluye un `docker-compose.yml` para orquestar todos los servicios.

### 📂 Estructura:
root/
├── docker-compose.yml
├── frontend/ (Flask)
├── ms-usuarios/ (FastAPI)
├── ms-fotos/ (FastAPI)
├── ms-carpetas/ (FastAPI)
└── minio/ (MinIO S3)


ms-usuarios/
    app/
    ├── api/                 ← Routers (entrada de API)
    │   └── v1/
    ├── core/                ← Configuración, seguridad, utilidades
    ├── db/                  ← Conexión, sesiones, base, migraciones
    ├── handlers/            ← Manejo de errores centralizados
    ├── models/              ← Modelos de SQLAlchemy
    ├── schemas/             ← Esquemas Pydantic (entrada y salida)
    ├── services/            ← Lógica de negocio
    ├── main.py              ← Punto de entrada


### 📥 Comando para levantar todo:
```bash
docker compose up --build
```
### 📥 Comando para levantar solo microservicios con su db:
```bash
docker compose --profile ms-usuarios up --build

docker compose --profile ms-fotos up --build
```

🖥️ Servicios disponibles:
Servicio	URL
> -Frontend	http://localhost:5000
> - API Usuarios	http://localhost:8000/docs  (Solo en funcionamiento)
> - API Fotos	http://localhost:8002/docs
> - API Carpetas	http://localhost:8003/docs
> - MinIO	http://localhost:9001



