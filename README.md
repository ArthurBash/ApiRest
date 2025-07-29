# 📸 Galería de Imágenes - Flask + FastAPI + Microservicios + MinIO + PostgreSQL

Proyecto de arquitectura moderna basado en microservicios, desarrollado con **Flask (Frontend)** y **FastAPI (Backend)**. Permite a los usuarios registrarse, iniciar sesión, subir imágenes, organizarlas en carpetas, filtrarlas por tags, nombre o fecha, y definir si son públicas o privadas.  
Todas las fotos son almacenadas en **MinIO (S3 compatible)**. La seguridad está implementada mediante **JWT**, contraseñas hasheadas y control de permisos.

---

## 🏛️ Arquitectura General
```
Frontend (Flask)
│
├──> Microservicio Usuarios (FastAPI + PostgreSQL) [JWT / Hash Passwords]
├──> Microservicio Fotos (FastAPI + PostgreSQL + MinIO S3)
└──> Microservicio Carpetas (FastAPI + MongoDB)
```

---

## 🚀 Cómo levantar el proyecto completo (Docker Compose)
Este proyecto incluye un `docker-compose.yml` para orquestar todos los servicios.

### 📂 Estructura:
```
root/
├── docker-compose.yml
├── frontend/ (Flask)
├── ms-usuarios/ (FastAPI)
├── ms-fotos/ (FastAPI)
├── ms-carpetas/ (FastAPI)
└── minio/ (MinIO S3)
```

```
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
```

### 🛠️ Comportamiento al iniciar ms-usuarios
Cuando se levanta el contenedor de ms-usuarios, se ejecuta el entrypoint definido en el servicio. Este entrypoint incluye una verificación para comprobar si existe un usuario de prueba en la base de datos PostgreSQL.
Si el usuario no existe, se crea automáticamente con los siguientes datos por defecto (pueden variar según configuración):

```
📛 Usuario:     admin
🔑 Contraseña:  admin1234
📧 Email:       admin@example.com

Este comportamiento facilita las pruebas locales y el desarrollo sin necesidad de registrar manualmente un usuario inicial.
```


> ℹ️ Podés modificar estos datos desde las variables de entorno definidas en el archivo .env.

### ⚙️ Configuración de entorno

Para cada microservicio, es necesario copiar el archivo de plantilla de entorno antes de ejecutar el proyecto:
```bash
cp env/env.template.ms-usuarios ms-usuarios/.env  
cp env/env.template.ms-fotos ms-fotos/.env
cp env/env.template.frontend frontend/.env
```

> 📌 Este paso es obligatorio, ya que los archivos .env están ignorados en el repositorio mediante .gitignore para evitar exponer credenciales sensibles.

### 📥 Comando para levantar todo:
```bash
docker compose up --build
```



🖥️ Servicios disponibles:
Servicio	URL
> - Frontend	http://localhost:5000               (funcionando)
> - API Usuarios	http://localhost:8000/docs  (funcionamiento)
> - API Fotos	http://localhost:8001/docs      (funcionando)
> - API Carpetas	http://localhost:8003/docs
> - MinIO	http://localhost:9001   (funcionando)



