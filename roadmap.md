# 🚀 Roadmap Proyecto Flask + FastAPI + Microservicios + MinIO + Postgres (MVP Backend First)

## ✅ Fase 1: Microservicio de Usuarios (COMPLETADO)
- [x] CRUD completo de usuarios
- [x] JWT para autenticación
- [x] Hasheo de contraseñas (CryptContext)
- [x] Hasheo de ID en las respuestas
- [x] Dockerfile + Postgres + .env configurados
- [x] Tests unitarios

---

## 🔨 Fase 2: Microservicio de Fotos (En Progreso)
**Objetivo:** Subir, almacenar y consultar fotos mediante MinIO S3.

### Estructura:
ms-fotos/app/
├── api/
│   ├── v1/
│   │   └── photos.py
│   └── deps.py
├── core/
│   ├── config.py
│   └── security.py
├── db/
│   ├── base.py
│   └── session.py
├── handler/
│   └── errors.py
├── models/
│   └── photo.py
├── schemas/
│   └── photo.py
├── services/
│   └── photo.py
├── exceptions.py
├── main.py
├── test/
│   └── photo.py
├── Dockerfile
├── requirements.txt
└── .env


### Checklist:
- [ ] Definir modelo `Photo` (nombre, path, usuario_id, carpeta_id, fecha, id hasheado)
- [ ] Endpoints CRUD básico: subir, listar, eliminar fotos
- [ ] Integración MinIO S3 para almacenamiento (presigned urls recomendadas)
- [ ] Seguridad: JWT tokens en endpoints
- [ ] Hasheo del ID en las respuestas
- [ ] Tests unitarios (pytest)
- [ ] Dockerfile + .env + Postgres funcionando

---

## 🔨 Fase 3: Microservicio de Carpetas
**Objetivo:** Organizar fotos en carpetas, gestionar permisos, tags y relaciones a usuarios.

### Estructura:
ms-carpetas/app/
├── api/v1/folders.py
├── api/deps.py
├── core/config.py
├── core/security.py
├── db/base.py
├── db/session.py
├── handler/errors.py
├── models/folder.py
├── schemas/folder.py
├── services/folder.py
├── exceptions.py
├── main.py
├── test/folder.py
├── Dockerfile
├── requirements.txt
└── .env


### Checklist:
- [ ] Definir modelo `Folder` (nombre, permisos, usuario_id, tags, fecha, id hasheado)
- [ ] CRUD de carpetas
- [ ] Implementar permisos (público / privado)
- [ ] Implementar tags (búsqueda simple por lista de strings)
- [ ] Endpoints para búsqueda por nombre / tags
- [ ] Seguridad: JWT tokens
- [ ] Hasheo de IDs
- [ ] Tests unitarios (pytest)
- [ ] Dockerfile + .env + Postgres funcionando

---

## 🔗 Fase 4: Integración de Microservicios
**Objetivo:** Verificar la comunicación e integración entre todos los microservicios.

### Checklist:
- [ ] Validar autenticación de usuarios mediante JWT (ms-usuarios)
- [ ] Asociar fotos correctamente a carpetas y usuarios (ms-fotos, ms-carpetas)
- [ ] Validar permisos de acceso a carpetas y fotos
- [ ] Probar flujos entre microservicios con Postman

---

## 🖥️ Fase 5: Frontend (Flask)
**Objetivo:** Renderizar páginas, gestionar sesión JWT, consumir APIs REST.

### Checklist:
- [ ] Implementar registro / login de usuarios (gestión JWT en cookies)
- [ ] Página principal: galería de imágenes (con ms-fotos y ms-carpetas)
- [ ] Formulario para subir fotos (a ms-fotos)
- [ ] Formulario para crear carpetas (a ms-carpetas)
- [ ] Implementar filtros (tags, nombre, fecha) en la galería
- [ ] Implementar logout

---

## 🛠️ Fase 6: Detalles Finales y Pulido
**Objetivo:** Mejorar calidad, seguridad y presentación para portafolio.

### Checklist:
- [ ] Validación exhaustiva de permisos
- [ ] Mejorar seguridad (CSRF tokens, Headers HTTP seguros)
- [ ] Mejorar estilos (Bootstrap u otro simple, galería clara)
- [ ] Documentar APIs (Swagger/OpenAPI por FastAPI)
- [ ] Documentar proyecto en README
- [ ] Agregar diagramas de arquitectura (opcional pero recomendado)
- [ ] Instrucciones claras de despliegue (Docker Compose opcional)

---

## 🎯 Entregable Final para Portafolio:
- [ ] 3 Microservicios separados, dockerizados, con sus bases de datos Postgres y MinIO
- [ ] Seguridad completa (JWT, hash contraseñas, hash ids)
- [ ] Frontend funcional: Login / Register / Upload / Browse / Filtros
- [ ] Proyecto documentado con capturas y diagramas

