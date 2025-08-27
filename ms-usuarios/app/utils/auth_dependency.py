from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.services.auth_service import AuthService
from app.schemas.user_schemas import TokenData
from app.exceptions import InvalidCredentialsError

security = HTTPBearer()


class AuthDependency:
    def __init__(self, auth_service: AuthService):
        self.auth_service = auth_service

    def get_current_user(self, credentials: HTTPAuthorizationCredentials = Depends(security)) -> TokenData:
        """Dependency para obtener usuario actual desde JWT"""
        try:
            token = credentials.credentials
            return self.auth_service.verify_token(token)
        except InvalidCredentialsError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido o expirado",
                headers={"WWW-Authenticate": "Bearer"},
            )
