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

router = APIRouter(prefix="/api/users", tags=["users"])

@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def api_create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    validate_unique_user(db, user_in.username, user_in.email)
    user = create_user(db, user_in)
    user.id = str(user.id)  
    return user

@router.get("/", response_model=List[UserRead])
def api_list_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()
    return [user_to_id_hasheado(u) for u in users]


@router.get("/{user_id}", response_model=UserRead)
def api_get_user(user = Depends(get_existing_user)):
    return user_to_id_hasheado(user)




@router.put("/{user_id}", response_model=UserRead)
def api_update_user(
    user_id: str,
    user_in: UserUpdatePUT,
    db: Session = Depends(get_db)
):
    user_db = get_existing_user(user_id,db)
    

    update_user(user_in,db,user_db)

    return user_to_id_hasheado(user_db)


@router.patch("/{user_id}", response_model=UserRead)
def api_update_user(
    user_id: str,
    user_in: UserUpdate,
    db: Session = Depends(get_db)
):
    user_db = get_existing_user(user_id,db)
    update_user(user_in,db,user_db)

    return user_to_id_hasheado(user_db)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def api_delete_user(user_db = Depends(get_existing_user),  db: Session = Depends(get_db)):
    delete_user(user_db,db)
    