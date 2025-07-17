# 📸 Galería de Imágenes - Flask + FastAPI + Microservicios + MinIO + PostgreSQL

Proyecto de arquitectura moderna basado en microservicios, desarrollado con **Flask (Frontend)** y **FastAPI (Backend)**. Permite a los usuarios registrarse, iniciar sesión, subir imágenes, organizarlas en carpetas, filtrarlas por tags, nombre o fecha, y definir si son públicas o privadas.  
Todas las fotos son almacenadas en **MinIO (S3 compatible)**. La seguridad está implementada mediante **JWT**, contraseñas hasheadas y control de permisos.

---

## 🏛️ Arquitectura General

Frontend (Flask)
│
├──> Microservicio Usuarios (FastAPI + PostgreSQL) [JWT / Hash Passwords]
├──> Microservicio Fotos (FastAPI + PostgreSQL + MinIO S3)
└──> Microservicio Carpetas (FastAPI + PostgreSQL)


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

### 📥 Comando para levantar todo:
```bash
docker-compose up --build
```

🖥️ Servicios disponibles:
Servicio	URL
Frontend	http://localhost:5000
API Usuarios	http://localhost:8000/docs  (Solo en funcionamiento)
API Fotos	http://localhost:8002/docs
API Carpetas	http://localhost:8003/docs
MinIO	http://localhost:9001

