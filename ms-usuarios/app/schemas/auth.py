from pydantic import BaseModel
from app.schemas.user import UserBase
# Modelo de salida que unifica UserRead y UserBase
class UserOut(UserBase):
    id: str

    model_config = {
        "from_attributes": True
    }

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserOut