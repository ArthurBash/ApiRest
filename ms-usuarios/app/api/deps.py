from fastapi import Depends, HTTPException, status,Path
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.services.user import get_user,decode_id


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_existing_user(user_id: str = Path(...), db: Session = Depends(get_db)):
    try:
        decoded_id = decode_id(user_id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Error en la decodificacion")

    user = get_user(db, decoded_id)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    return user