from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.schemas.user import UserCreate, UserRead, UserUpdate,UserUpdatePUT
from app.models.user import User
from app.services.user import (
    create_user, get_user, get_user_by_username,
    update_user,delete_user,get_user_by_email,
    validate_unique_user,user_to_id_hasheado)
from app.api.deps import get_db,get_existing_user
from fastapi import HTTPException

from app.core.security import authenticate_user,create_access_token,get_current_user
from datetime import timedelta
from app.schemas.auth import Token


from fastapi.security import OAuth2PasswordRequestForm



router = APIRouter(prefix="/api/users", tags=["users"])

@router.get("/me", response_model=UserRead)
async def read_users_me(
    current_user: User = Depends(get_current_user)
    ):
    return user_to_id_hasheado(current_user)

@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def api_create_user(
    user_in: UserCreate, db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):
    validate_unique_user(db, user_in.username, user_in.email)
    user = create_user(db, user_in)
    return user_to_id_hasheado(user)

@router.get("/", response_model=List[UserRead])
def api_list_users(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):
    users = db.query(User).offset(skip).limit(limit).all()
    return [user_to_id_hasheado(u) for u in users]


@router.get("/{user_id}", response_model=UserRead)
def api_get_user(
    user = Depends(get_existing_user),
    current_user: User = Depends(get_current_user)):
    return user_to_id_hasheado(user)



@router.put("/{user_id}", response_model=UserRead)
def api_update_user(
    user_id: str,
    user_in: UserUpdatePUT,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user_db = get_existing_user(user_id,db)
    

    update_user(user_in,db,user_db)

    return user_to_id_hasheado(user_db)


@router.patch("/{user_id}", response_model=UserRead)
def api_update_user(
    user_id: str,
    user_in: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user_db = get_existing_user(user_id,db)
    update_user(user_in,db,user_db)

    return user_to_id_hasheado(user_db)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def api_delete_user(user_db = Depends(get_existing_user),  db: Session = Depends(get_db),
current_user: User = Depends(get_current_user)):
    delete_user(user_db,db)


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)): 
    username = form_data.username
    password = form_data.password
    user = authenticate_user(username, password,db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña Incorrecta",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(subject=user.username, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


