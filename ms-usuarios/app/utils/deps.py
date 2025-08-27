from fastapi import Depends                
from sqlalchemy.orm import Session        
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService
from app.services.auth_service import AuthService
from app.controllers.user_controller import UserController
from app.utils.auth_dependency import AuthDependency
from app.schemas.user_schemas import TokenData 
from typing import Generator
from app.db.session import SessionLocal 

# Dependency Injection

def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db)


def get_user_service(
    user_repository: UserRepository = Depends(get_user_repository)
) -> UserService:
    return UserService(user_repository)


def get_auth_service(
    user_service: UserService = Depends(get_user_service)
) -> AuthService:
    return AuthService(user_service)


def get_user_controller(
    user_service: UserService = Depends(get_user_service),
    auth_service: AuthService = Depends(get_auth_service)
) -> UserController:
    return UserController(user_service, auth_service)


def get_auth_dependency(
    auth_service: AuthService = Depends(get_auth_service)
) -> AuthDependency:
    return AuthDependency(auth_service)


def get_current_user(
    auth_dep: AuthDependency = Depends(get_auth_dependency)
) -> TokenData:
    """Dependency para obtener usuario actual"""
    return auth_dep.get_current_user
