class BaseCustomException(Exception):
    def __init__(self, message: str, **kwargs):
        self.message = message
        self.extra_data = kwargs
        super().__init__(self.message)


class UserNotFoundError(BaseCustomException):
    def __init__(self, user_id: str = None, identifier: str = None):
        self.user_id = user_id
        self.identifier = identifier
        if user_id:
            message = f"Usuario con ID {user_id} no fue encontrado"
        elif identifier:
            message = f"Usuario {identifier} no fue encontrado"
        else:
            message = "Usuario no encontrado"
        super().__init__(message, user_id=user_id, identifier=identifier)


class UserAlreadyExistsError(BaseCustomException):
    def __init__(self, field: str, value: str):
        self.field = field
        self.value = value
        message = f"Ya existe un usuario con {field}: {value}"
        super().__init__(message, field=field, value=value)


class InvalidCredentialsError(BaseCustomException):
    def __init__(self):
        super().__init__("Credenciales inválidas")


class RateLimitError(BaseCustomException):
    def __init__(self, retry_after: int):
        self.retry_after = retry_after
        message = f"Demasiados intentos. Inténtalo de nuevo en {retry_after} segundos"
        super().__init__(message, retry_after=retry_after)