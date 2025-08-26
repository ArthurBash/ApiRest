from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY,HTTP_404_NOT_FOUND,HTTP_400_BAD_REQUEST
from fastapi import FastAPI
from app.exceptions import DecodingError,PhotoNotFoundError,FileNotValidate,FolderNotFoundError

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
    @app.exception_handler(DecodingError)
    async def error_decodificacion(request: Request, exc: DecodingError):
        return JSONResponse(
            status_code=HTTP_404_NOT_FOUND,
            content={"detail": "Error en la decodificacion"},
        )
    
    @app.exception_handler(PhotoNotFoundError)
    async def error_foto_no_encontrada(request: Request, exc: PhotoNotFoundError):
        return JSONResponse(
            status_code=HTTP_404_NOT_FOUND,
            content={"detail": "Foto no encontrada"},
        )

    @app.exception_handler(FileNotValidate)
    async def error_imagen_no_valida(request: Request, exc: FileNotValidate):
        return JSONResponse(
            status_code=HTTP_400_BAD_REQUEST,
            content={"detail": "Archivo no es una imagen válida"},
        )

    @app.exception_handler(FolderNotFoundError)
    async def error_carpeta_no_encontrada(request: Request, exc: FolderNotFoundError):
        return JSONResponse(
            status_code=HTTP_404_NOT_FOUND,
            content={"detail": f"Folder con ID {exc.folder_id} no fue encontrado o no está activo"},
        )




