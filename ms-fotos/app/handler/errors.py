from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY,HTTP_404_NOT_FOUND
from fastapi import FastAPI
from app.exceptions import ErrorDecodificacion,ErrorFotoNoEncontrada

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

        @app.exception_handler(ErrorDecodificacion)
        async def error_decodificacion(request: Request, exc: ErrorDecodificacion):
            return JSONResponse(
                status_code=HTTP_404_NOT_FOUND,
                content={"detail": "Error en la decodificacion"},
            )
        
        @app.exception_handler(ErrorFotoNoEncontrada)
        async def error_foto_no_encontrada(request: Request, exc: ErrorFotoNoEncontrada):
            return JSONResponse(
                status_code=HTTP_404_NOT_FOUND,
                content={"detail": "Foto no encontrada"},
            )

