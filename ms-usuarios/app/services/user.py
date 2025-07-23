from sqlalchemy.orm import Session
from app.models.user import User as UserModel
from app.schemas.user import UserCreate,UserRead,UserUpdate,UserUpdatePUT
from app.exceptions import UsernameAlreadyExists, EmailAlreadyExists

from passlib.context import CryptContext

# app/services/hashid_service.py
from hashids import Hashids
import os
from dotenv import load_dotenv


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user(db: Session, user_id: int):
    return db.query(UserModel).filter(UserModel.id == user_id).first()

def get_users(db: Session):
    users = db.query(User).offset(skip).limit(limit).all()
    return users


def get_user_by_username(db: Session, username: str):
    return db.query(UserModel).filter(UserModel.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(UserModel).filter(UserModel.email == email).first()


def create_user(db: Session, user_in: UserCreate):
    hashed_pw = pwd_context.hash(user_in.password)
    db_user = UserModel(
        name=user_in.name,
        lastname=user_in.lastname,
        username=user_in.username,
        email=user_in.email,
        hashed_password=hashed_pw,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user_patch(user_db, user_in: UserUpdate, db: Session):
    user_data = user_in.dict(exclude_unset=True)  # Solo campos enviados

    for field, value in user_data.items():
        setattr(user_db, field, value)

    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db

def update_user_put(user_db, user_in: UserUpdatePUT, db: Session):
    user_db.name = user_in.name
    user_db.lastname = user_in.lastname
    user_db.username = user_in.username
    user_db.email = user_in.email
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db

def delete_user(user_db,db):
    db.delete(user_db)
    db.commit()

def validate_unique_user(db, username: str, email: str):
    if get_user_by_username(db, username):
        raise UsernameAlreadyExists()
    if get_user_by_email(db, email):
        raise EmailAlreadyExists()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

load_dotenv() 

HASHIDS_SALT = os.getenv("HASHIDS_SALT", "valor_por_defecto_no_conveniente")
HASHIDS_MIN_LENGTH = int(os.getenv("HASHIDS_MIN_LENGTH", 8))

hashids = Hashids(salt=HASHIDS_SALT, min_length=HASHIDS_MIN_LENGTH)

def encode_id(id: int) -> str:
    return hashids.encode(id)

def decode_id(hashid: str) -> int:
    decoded = hashids.decode(hashid)
    if decoded:
        return decoded[0]
    raise ValueError("ID inválido")

def user_to_id_hasheado(user) -> UserRead:
    return UserRead(
        id= encode_id(user.id),   
        username = user.username,
        name = user.name,
        lastname= user.lastname,
        email= user.email,
    )