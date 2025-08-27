import os
import logging
from app.repositories.user_repository import UserRepository
from app.schemas.user_schemas import UserCreate
from app.services.user_service import UserService
from app.utils.deps import get_db

def create_initial_user():
    # Obtener sesión de DB
    db_gen = get_db()
    db = next(db_gen)
    try:
        user_repository = UserRepository(db)
        user_service = UserService(user_repository)

        username = os.getenv("INITIAL_USER_USERNAME")
        email = os.getenv("INITIAL_USER_EMAIL")

        existing_user = user_repository.get_by_username_or_email(username)
        if existing_user:
            logging.info("Usuario inicial ya existe")
            return

        # Crear usuario inicial
        user_data = UserCreate(
            name=os.getenv("INITIAL_USER_NAME"),
            lastname=os.getenv("INITIAL_USER_LASTNAME"),
            username=username,
            password=os.getenv("INITIAL_USER_PASSWORD"),
            email=email,
        )

        user_service.create_user(user_data)
        logging.info("Usuario inicial creado")
    finally:
        db.close()


if __name__ == "__main__":
    create_initial_user()
