from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from app.exceptions import BaseCustomException, DecodingError, PhotoNotFoundError, FileNotValidate, FolderNotFoundError

def register_exception_handlers(app: FastAPI):

    # Handler base    
    @app.exception_handler(BaseCustomException)
    def base_custom_exception_handler(request: Request, exc: BaseCustomException):
        return JSONResponse(
            status_code=HTTP_400_BAD_REQUEST,
            content={
                "detail": exc.message,
                "success": False,
                **getattr(exc, "extra_data", {})
            },
        )

    @app.exception_handler(DecodingError)
    def decoding_error_handler(request: Request, exc: DecodingError):
        return JSONResponse(
            status_code=HTTP_404_NOT_FOUND,
            content={
                "detail": "Error en la decodificación",
                "success": False,
                **getattr(exc, "extra_data", {})
            },
        )

    @app.exception_handler(PhotoNotFoundError)
    def photo_not_found_handler(request: Request, exc: PhotoNotFoundError):
        return JSONResponse(
            status_code=HTTP_404_NOT_FOUND,
            content={
                "detail": "Foto no encontrada",
                "success": False,
                **getattr(exc, "extra_data", {})
            },
        )

    @app.exception_handler(FileNotValidate)
    def file_not_valid_handler(request: Request, exc: FileNotValidate):
        return JSONResponse(
            status_code=HTTP_400_BAD_REQUEST,
            content={
                "detail": "Archivo no es una imagen válida",
                "success": False,
                **getattr(exc, "extra_data", {})
            },
        )

    @app.exception_handler(FolderNotFoundError)
    def folder_not_found_handler(request: Request, exc: FolderNotFoundError):
        return JSONResponse(
            status_code=HTTP_404_NOT_FOUND,
            content={
                "detail": f"Folder con ID {exc.folder_id} no fue encontrado o no está activo",
                "success": False,
                **getattr(exc, "extra_data", {})
            },
        )
