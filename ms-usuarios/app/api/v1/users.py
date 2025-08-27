import uuid
from typing import List

from fastapi import APIRouter, Depends, Query, Path, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Security

from app.utils.deps import (
    get_user_repository,
    get_user_service,
    get_auth_service,
    get_user_controller,
    get_auth_dependency,
    get_current_user,
)

from app.controllers.user_controller import UserController
from app.schemas.user_schemas import UserCreate, UserUpdate, UserRead, UserLogin, Token, TokenData

router = APIRouter(
    prefix="/api/v1/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/token/login")

@router.get("/me", response_model=UserRead)
def get_current_user_info(
    controller: UserController = Depends(get_user_controller),
    current_user: TokenData = Security(get_current_user)
):
    """
    Obtener información del usuario autenticado actual
    
    Requiere token JWT válido en el header Authorization.
    """
    return controller.get_current_user_info(current_user)


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(
    user_data: UserCreate,
    controller: UserController = Depends(get_user_controller)
):
    """
    Crear un nuevo usuario
    
    - **name**: Nombre del usuario (2-100 caracteres)
    - **lastname**: Apellido del usuario (2-100 caracteres)
    - **username**: Username único (3-50 caracteres, solo letras, números y _)
    - **email**: Email válido
    - **password**: Contraseña (mínimo 8 caracteres, al menos 2 números y 1 carácter especial)
    """
    return controller.create_user(user_data)


@router.get("/", response_model=List[UserRead])
def get_all_users(
    skip: int = Query(0, ge=0, description="Número de elementos a saltar"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de elementos a retornar"),
    controller: UserController = Depends(get_user_controller),
    current_user: TokenData = Security(get_current_user)
):
    """
    Obtener todos los usuarios (paginado)
    
    - **skip**: Offset para paginación
    - **limit**: Límite de elementos por página
    
    Requiere autenticación JWT.
    """
    return controller.get_all_users(skip=skip, limit=limit)


@router.get("/{user_id}", response_model=UserRead)
def get_user_by_id(
    user_id: uuid.UUID = Path(..., description="UUID del usuario"),
    controller: UserController = Depends(get_user_controller),
    current_user: TokenData = Security(get_current_user)
):
    """
    Obtener usuario por UUID
    
    - **user_id**: UUID del usuario
    
    Requiere autenticación JWT.
    """
    return controller.get_user_by_id(user_id)


@router.put("/{user_id}", response_model=UserRead)
def update_user(
    user_id: uuid.UUID = Path(..., description="UUID del usuario"),
    user_data: UserUpdate = None,
    controller: UserController = Depends(get_user_controller),
    current_user: TokenData = Security(get_current_user)
):
    """
    Actualizar completamente un usuario
    
    - **user_id**: UUID del usuario
    - **name**: Nuevo nombre (opcional)
    - **lastname**: Nuevo apellido (opcional)
    - **username**: Nuevo username (opcional)
    - **email**: Nuevo email (opcional)
    - **password**: Nueva contraseña (opcional)
    
    Requiere autenticación JWT.
    """
    return controller.update_user(user_id, user_data)


@router.patch("/{user_id}", response_model=UserRead)
def partial_update_user(
    user_id: uuid.UUID = Path(..., description="UUID del usuario"),
    user_data: UserUpdate = None,
    controller: UserController = Depends(get_user_controller),
    current_user: TokenData = Security(get_current_user)
):
    """
    Actualizar parcialmente un usuario
    
    Solo se actualizarán los campos proporcionados.
    
    - **user_id**: UUID del usuario
    - **name**: Nuevo nombre (opcional)
    - **lastname**: Nuevo apellido (opcional)
    - **username**: Nuevo username (opcional)
    - **email**: Nuevo email (opcional)
    - **password**: Nueva contraseña (opcional)
    
    Requiere autenticación JWT.
    """
    return controller.partial_update_user(user_id, user_data)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: uuid.UUID = Path(..., description="UUID del usuario"),
    controller: UserController = Depends(get_user_controller),
    current_user: TokenData = Security(get_current_user)
):
    """
    Eliminar usuario permanentemente
    
    - **user_id**: UUID del usuario a eliminar
    
    Requiere autenticación JWT.
    """
    controller.delete_user(user_id)


@router.post("/token/login", response_model=Token)
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    controller: UserController = Depends(get_user_controller)
):
    """
    Autenticar usuario y obtener token JWT
    
    - **username**: Username o email del usuario
    - **password**: Contraseña del usuario
    
    Retorna un token JWT válido por 30 minutos.
    Rate limited: máximo 5 intentos por minuto por IP.
    """
    login_data = UserLogin(username=form_data.username, password=form_data.password)

    return controller.login_user(login_data)
