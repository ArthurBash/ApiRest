import uuid
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy import or_
from app.models.user import User
from app.exceptions import UserNotFoundError, UserAlreadyExistsError


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user_data: dict) -> User:
        """Crear un nuevo usuario"""
        try:
            user = User(**user_data)
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            return user
        except IntegrityError as e:
            self.db.rollback()
            if "username" in str(e.orig) or "user" in str(e.orig):
                raise UserAlreadyExistsError("username", user_data.get("username"))
            elif "email" in str(e.orig):
                raise UserAlreadyExistsError("email", user_data.get("email"))
            raise e
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e

    def get_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        """Obtener usuario por ID"""
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_username(self, username: str) -> Optional[User]:
        """Obtener usuario por username"""
        return self.db.query(User).filter(User.username == username).first()

    def get_by_email(self, email: str) -> Optional[User]:
        """Obtener usuario por email"""
        return self.db.query(User).filter(User.email == email).first()

    def get_by_username_or_email(self, identifier: str) -> Optional[User]:
        """Obtener usuario por username o email"""
        return self.db.query(User).filter(
            or_(User.username == identifier, User.email == identifier)
        ).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Obtener todos los usuarios"""
        return self.db.query(User).offset(skip).limit(limit).all()

    def update(self, user_id: uuid.UUID, update_data: dict) -> User:
        """Actualizar usuario"""
        user = self.get_by_id(user_id)
        if not user:
            raise UserNotFoundError(user_id=str(user_id))
        
        try:
            for key, value in update_data.items():
                if hasattr(user, key):
                    setattr(user, key, value)
            
            self.db.commit()
            self.db.refresh(user)
            return user
        except IntegrityError as e:
            self.db.rollback()
            if "username" in str(e.orig) or "user" in str(e.orig):
                raise UserAlreadyExistsError("username", update_data.get("username"))
            elif "email" in str(e.orig):
                raise UserAlreadyExistsError("email", update_data.get("email"))
            raise e
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e

    def delete(self, user_id: uuid.UUID) -> bool:
        """Eliminar usuario permanentemente"""
        user = self.get_by_id(user_id)
        if not user:
            raise UserNotFoundError(user_id=str(user_id))
        
        try:
            self.db.delete(user)
            self.db.commit()
            return True
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e

    def exists_by_username(self, username: str) -> bool:
        """Verificar si existe usuario con username"""
        return self.db.query(User).filter(User.username == username).first() is not None

    def exists_by_email(self, email: str) -> bool:
        """Verificar si existe usuario con email"""
        return self.db.query(User).filter(User.email == email).first() is not None
