from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.exceptions import EmailAlreadyExists,UsernameAlreadyExists,UserOrPasswordError
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY,HTTP_401_UNAUTHORIZED,HTTP_400_BAD_REQUEST
from fastapi import FastAPI

def register_exception_handlers(app: FastAPI):

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        errors = exc.errors()
        error_messages = []
        for err in errors:
            loc = " -> ".join(str(x) for x in err['loc'])
            msg = err['msg']
            error_messages.append(f"Error en {loc}: {msg}")

        return JSONResponse(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "detail": "No pasó las validaciones requeridas.",
                "errors": error_messages,
            },
        )

    @app.exception_handler(UsernameAlreadyExists)
    async def username_exists_handler(request: Request, exc: UsernameAlreadyExists):
        return JSONResponse(
            status_code=HTTP_400_BAD_REQUEST,
            content={"detail": "Nombre de usuario existente"},
        )

    @app.exception_handler(EmailAlreadyExists)
    async def email_exists_handler(request: Request, exc: EmailAlreadyExists):
        return JSONResponse(
            status_code=HTTP_400_BAD_REQUEST,
            content={"detail": "Email ya existente"},
        )
    
    @app.exception_handler(UserOrPasswordError)
    async def email_exists_handler(request: Request, exc: UserOrPasswordError):
        return JSONResponse(
            status_code=HTTP_401_UNAUTHORIZED,
            content={"detail": "Usuario o contraseña incorrectos"},
        )