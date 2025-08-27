from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.status import (
    HTTP_422_UNPROCESSABLE_ENTITY, 
    HTTP_404_NOT_FOUND, 
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_429_TOO_MANY_REQUESTS,
    HTTP_500_INTERNAL_SERVER_ERROR
)
from app.exceptions import (
    UserNotFoundError, UserAlreadyExistsError, InvalidCredentialsError, RateLimitError
)


def register_user_exception_handlers(app: FastAPI):
    """Registrar manejadores de excepciones para usuarios"""

    @app.exception_handler(RequestValidationError)
    def validation_exception_handler(request: Request, exc: RequestValidationError):
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

    @app.exception_handler(UserNotFoundError)
    def user_not_found_handler(request: Request, exc: UserNotFoundError):
        return JSONResponse(
            status_code=HTTP_404_NOT_FOUND,
            content={
                "detail": exc.message,
                "user_id": exc.user_id,
                "identifier": exc.identifier
            }
        )

    @app.exception_handler(UserAlreadyExistsError)
    def user_already_exists_handler(request: Request, exc: UserAlreadyExistsError):
        return JSONResponse(
            status_code=HTTP_400_BAD_REQUEST,
            content={
                "detail": exc.message,
                "field": exc.field,
                "value": exc.value
            }
        )

    @app.exception_handler(InvalidCredentialsError)
    def invalid_credentials_handler(request: Request, exc: InvalidCredentialsError):
        return JSONResponse(
            status_code=HTTP_401_UNAUTHORIZED,
            content={
                "detail": exc.message
            },
            headers={"WWW-Authenticate": "Bearer"}
        )

    @app.exception_handler(RateLimitError)
    def rate_limit_handler(request: Request, exc: RateLimitError):
        return JSONResponse(
            status_code=HTTP_429_TOO_MANY_REQUESTS,
            content={
                "detail": exc.message,
                "retry_after": exc.retry_after
            },
            headers={"Retry-After": str(exc.retry_after)}
        )