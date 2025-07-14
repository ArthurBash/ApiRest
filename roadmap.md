# Hoja de Ruta - Proyecto API REST

## Descripción del Proyecto

API REST completa desarrollada con Flask para la  de usuarios. La autenticación y autorización se realizan mediante tokens JWT. Los datos se almacenan en bases de datos PostgreSQL y MongoDB, accesibles mediante diferentes endpoints o parámetros según la necesidad. El proyecto está completamente dockerizado, con entornos separados para desarrollo y producción, e integra Redis para el manejo eficiente de caché y mejora del rendimiento. Dispone de documentación interactiva generada con Swagger para facilitar el consumo y la comprensión de la API.
---

## Fase 1: Configuración Inicial y Estructura Base (Días 1-3)

### 1.1 Crear Estructura del Proyecto
```
proyecto-apirest/
├── app/
│   ├── __init__.py
│   ├── app.py
│   ├── config.py
│   ├── controllers/
│   │   ├── __init__.py
│   │   └── user_controller.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── user_service.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py
│   ├── extensions.py
│   ├── middlewares/
│   │   ├── __init__.py
│   │   └── logging.py
│   └── utils/
├── tests/
├── requirements.txt
├── Dockerfile
└── docker-compose.yml

```

### 1.2 Configuración Docker
- Crear `Dockerfile` para la aplicación Flask
- Configurar `docker-compose.yml` con servicios:
  - Flask app
  - PostgreSQL
  - MongoDB
  - Redis (para caché)
- Crear script `start.sh` para levantar la base de datos de prueba

### 1.3 Configuración Inicial de Flask
- Instalar dependencias: Flask, Flask-JWT-Extended, SQLAlchemy, PyMongo, etc.
- Configurar estructura básica de la aplicación
- Establecer configuraciones para diferentes entornos (.env)

---

## Fase 2: Base de Datos y Modelos (Días 4-6)

### 2.1 Configuración PostgreSQL
- Crear esquemas de base de datos
- Configurar SQLAlchemy con Flask
- Implementar modelos básicos (User)
- Configurar migraciones con Flask-Migrate

### 2.2 Configuración MongoDB
- Establecer conexión con PyMongo
- Crear modelos/esquemas para MongoDB
- Implementar `mongo_models.py` con funciones CRUD básicas

### 2.3 Testing de Base de Datos
- Configurar base de datos de prueba
- Tests básicos de conexión y modelos

---

## Fase 3: Autenticación y Autorización (Días 7-9)

### 3.1 Implementar JWT
- Configurar Flask-JWT-Extended
- Crear endpoints de autenticación:
  - `POST /auth/register` - Registro de usuarios
  - `POST /auth/login` - Login y generación de tokens
  - `POST /auth/refresh` - Renovar tokens
  - `POST /auth/logout` - Logout

### 3.2 Middleware de Autenticación
- Decoradores para proteger endpoints
- Manejo de roles y permisos
- Validación de tokens

### 3.3 Endpoint de Salud
- `GET /health` - Health check básico
- Verificar conexiones a bases de datos
- Status de servicios

---

## Fase 4: CRUD Completo (Días 10-14)

### 4.1 Endpoints PostgreSQL
- `GET /users/sql` - Listar usuarios
- `POST /users/sql` - Crear usuario
- `PUT /users/sql/:id` - Actualizar usuario
- `DELETE /users/sql/:id` - Eliminar usuario

### 4.2 Endpoints MongoDB
- `GET /users/mongo` - Listar documentos
- `POST /users/mongo` - Crear documento
- `PUT /users/mongo/:id` - Actualizar documento
- `DELETE /users/mongo/:id` - Eliminar documento

### 4.3 Rutas Avanzadas (/users/mongo)
- Completar todas las funciones en `mongo_models.py`
- Implementar filtros y paginación
- Manejo de errores específicos de MongoDB

---

## Fase 5: Documentación API (Días 15-16)

### 5.1 Integrar Swagger
- Instalar Flask-RESTX o Flasgger
- Documentar todos los endpoints
- Incluir esquemas de request/response
- Configurar UI de Swagger accesible

### 5.2 Documentación del Proyecto
- README.md completo
- Guías de instalación y uso
- Ejemplos de requests
- Documentación de la arquitectura

---

## Fase 6: Testing Automatizado (Días 17-19)

### 6.1 Tests con PyTest
- Configurar pytest y fixtures
- Tests unitarios para cada endpoint
- Tests de integración
- Tests de autenticación y autorización

### 6.2 Tests de CRUD
- Cobertura completa de operaciones
- Tests de casos edge
- Validación de respuestas y códigos de estado

### 6.3 Tests de Base de Datos
- Tests específicos para PostgreSQL
- Tests específicos para MongoDB
- Tests de conexiones y transacciones

---

## Fase 7: Validación y Mejoras (Días 20-22)

### 7.1 Validación de Entrada
- Implementar marshmallow o pydantic
- Validación de JSON de entrada
- Manejo robusto de errores

### 7.2 Logging Estructurado
- Configurar logging centralizado
- Logs de requests/responses
- Logs de errores y excepciones
- Integración con middleware

### 7.3 Manejo de Errores Centralizado
- Middleware para manejo de errores
- Respuestas consistentes de error
- Logging de errores críticos

---

## Fase 8: Optimización y Deployment (Días 23-25)

### 8.1 Optimizaciones
- Caché con Redis
- Optimización de queries
- Paginación eficiente
- Rate limiting

### 8.2 Configuración de Producción
- Variables de entorno de producción
- Configuración de seguridad
- SSL/TLS
- Monitoreo básico

### 8.3 CI/CD Básico
- GitHub Actions o GitLab CI
- Tests automatizados en pipeline
- Build y push de imágenes Docker

---

## Tecnologías y Dependencias Principales

### Backend
- **Flask** - Framework web
- **Flask-JWT-Extended** - Autenticación JWT
- **SQLAlchemy** - ORM para PostgreSQL
- **PyMongo** - Driver MongoDB
- **Flask-RESTX** - Documentación Swagger
- **Marshmallow** - Serialización/validación

### Base de Datos
- **PostgreSQL** - Base de datos relacional
- **MongoDB** - Base de datos NoSQL
- **Redis** - Caché y sesiones

### Testing
- **PyTest** - Framework de testing
- **Factory Boy** - Fixtures de datos
- **pytest-cov** - Cobertura de código

### DevOps
- **Docker** - Containerización
- **Docker Compose** - Orquestación local
- **Gunicorn** - Servidor WSGI de producción

---

## Entregables por Fase

1. **Estructura y Docker** - Proyecto dockerizado funcional
2. **Base de Datos** - Modelos y conexiones establecidas
3. **Autenticación** - JWT implementado y endpoint de salud
4. **CRUD Completo** - Todos los endpoints funcionando
5. **Documentación** - Swagger integrado y docs completas
6. **Testing** - Suite de tests automatizados
7. **Validación** - API robusta con manejo de errores
8. **Producción** - Aplicación lista para deploy

---

## Comandos Útiles

```bash
# Levantar entorno de desarrollo
./start.sh

# Ejecutar tests
docker-compose exec app pytest

# Ver logs
docker-compose logs -f app

# Acceder a contenedor
docker-compose exec app bash

# Backup de datos
docker-compose exec postgres pg_dump -U user dbname > backup.sql
```

---


# ApiRest
Este proyecto es una API REST construida con Flask que permite realizar operaciones CRUD autenticadas con JWT. Permite guardar datos en PostgreSQL (estructurado) o MongoDB (documental).


portfolio-app/
├── .github/                  # Config CI/CD (opcional)
│   └── workflows/
├── infra/                    # Configuración infra
│   ├── docker-compose.yml    # Orquestación completa
│   └── minio/                # Config buckets (si aplica)
│
├── ms-usuarios/              # Microservicio 1
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py           # Lógica principal
│   │   ├── models.py         # DB models
│   │   └── schemas.py        # Pydantic
│   ├── tests/                # Pruebas
│   ├── Dockerfile
│   └── requirements.txt
│
├── ms-carpetas/              # Microservicio 2 (misma estructura)
├── ms-fotos/                 # Microservicio 3 
│
├── app-flask/                # Frontend
│   ├── static/               # CSS/JS
│   ├── templates/            # HTML
│   ├── app.py                # Flask core
│   ├── Dockerfile
│   └── requirements.txt
│
├── docs/                     # Documentación
│   ├── api.md                # Especificaciones
│   └── setup-guide.md
│
└── README.md                 # Punto de entrada