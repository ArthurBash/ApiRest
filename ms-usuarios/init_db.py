import os
from sqlalchemy.orm import Session
from app.models.user import User
from app.db.base import Base

from app.api.deps import get_db
from app.db.session import engine
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

from app.core.security import get_password_hash
# from app.services.user import validate_unique_user

import logging

def create_initial_user(db: Session):
    username = os.getenv("INITIAL_USER_USERNAME")
    if db.query(User).filter(User.username == username).first():
        logging.info("Usuario inicial ya existe")
        return

    

    hashed_password = get_password_hash(os.getenv("INITIAL_USER_PASSWORD"))

    new_user = User(
        name=os.getenv("INITIAL_USER_NAME"),
        lastname=os.getenv("INITIAL_USER_LASTNAME"),
        username=username,
        hashed_password=hashed_password,
        email=os.getenv("INITIAL_USER_EMAIL"),
    )
    db.add(new_user)
    db.commit()
    logging.info("Usuario inicial creado")




if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)  # crea tablas
    db = next(get_db())
    create_initial_user(db)