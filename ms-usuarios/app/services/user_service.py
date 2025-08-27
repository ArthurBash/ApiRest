import uuid
from typing import List
from app.repositories.user_repository import UserRepository
from app.schemas.user_schemas import UserCreate, UserUpdate, UserRead
from app.exceptions import UserNotFoundError, InvalidCredentialsError
from app.utils.password_utils import PasswordUtils


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        self.password_utils = PasswordUtils()

    def create_user(self, user_data: UserCreate) -> UserRead:
        """Crear nuevo usuario"""
        hashed_password = self.password_utils.hash_password(user_data.password)
        
        # Crear diccionario sin la contraseña plana
        user_dict = user_data.model_dump(exclude={'password'})
        user_dict['hashed_password'] = hashed_password
        
        user = self.user_repository.create(user_dict)
        return UserRead.model_validate(user)

    def get_user_by_id(self, user_id: uuid.UUID) -> UserRead:
        """Obtener usuario por ID"""
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundError(user_id=str(user_id))
        
        return UserRead.model_validate(user)

    def get_all_users(self, skip: int = 0, limit: int = 100) -> List[UserRead]:
        """Obtener todos los usuarios"""
        users = self.user_repository.get_all(skip=skip, limit=limit)
        return [UserRead.model_validate(user) for user in users]

    def update_user(self, user_id: uuid.UUID, user_data: UserUpdate) -> UserRead:
        """Actualizar usuario"""

        existing_user = self.user_repository.get_by_id(user_id)
        if not existing_user:
            raise UserNotFoundError(user_id=str(user_id))
        
        # Preparar datos de actualización
        update_dict = user_data.model_dump(exclude_unset=True)
        
        if 'password' in update_dict:
            hashed_password = self.password_utils.hash_password(update_dict['password'])
            update_dict['hashed_password'] = hashed_password
            del update_dict['password']  # Remover contraseña plana
        
        updated_user = self.user_repository.update(user_id, update_dict)
        return UserRead.model_validate(updated_user)

    def delete_user(self, user_id: uuid.UUID) -> bool:
        """Eliminar usuario"""
        return self.user_repository.delete(user_id)

    def authenticate_user(self, username_or_email: str, password: str) -> UserRead:
        """Autenticar usuario con username/email y contraseña"""

        user = self.user_repository.get_by_username_or_email(username_or_email)
        if not user:
            raise InvalidCredentialsError()
        
        if not self.password_utils.verify_password(password, user.hashed_password):
            raise InvalidCredentialsError()
        
        return UserRead.model_validate(user)