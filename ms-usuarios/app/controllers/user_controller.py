# controllers/user_controller.py
import uuid
from typing import List
from app.services.user_service import UserService
from app.services.auth_service import AuthService
from app.schemas.user_schemas import UserCreate, UserUpdate, UserRead, UserLogin, Token, TokenData


class UserController:
    def __init__(self, user_service: UserService, auth_service: AuthService):
        self.user_service = user_service
        self.auth_service = auth_service

    def create_user(self, user_data: UserCreate) -> UserRead:
        return self.user_service.create_user(user_data)

    def get_current_user_info(self, current_user: TokenData) -> UserRead:
        return self.user_service.get_user_by_id(current_user.user_id)

    def get_user_by_id(self, user_id: uuid.UUID) -> UserRead:
        return self.user_service.get_user_by_id(user_id)

    def get_all_users(self, skip: int = 0, limit: int = 100) -> List[UserRead]:
        return self.user_service.get_all_users(skip=skip, limit=limit)

    def update_user(self, user_id: uuid.UUID, user_data: UserUpdate) -> UserRead:
        return self.user_service.update_user(user_id, user_data)

    def partial_update_user(self, user_id: uuid.UUID, user_data: UserUpdate) -> UserRead:
        # Reutilizar la lógica de update_user
        return self.update_user(user_id, user_data)

    def delete_user(self, user_id: uuid.UUID) -> None:
        return self.user_service.delete_user(user_id)

    def login_user(self, login_data: UserLogin) -> Token:
        return self.auth_service.login_user(login_data.username, login_data.password)
