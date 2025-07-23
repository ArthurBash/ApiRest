from pydantic import BaseModel, EmailStr, Field
from typing import Optional


from typing import Optional


class UserUpdate(BaseModel):
    name: Optional[str] = Field(default=None)
    lastname: Optional[str] = Field(default=None)
    username: Optional[str] = Field(default=None)
    email: Optional[EmailStr] = Field(default=None)

class UserUpdatePUT(BaseModel):
    name: str
    lastname: str
    username: str
    email: EmailStr

class UserBase(BaseModel):
    name: str = Field(..., example="Arturo")
    lastname: str = Field(..., example="Wettstein")
    username: str = Field(..., example="artur")
    email: EmailStr = Field(..., example="arturo@gmail.com")


class UserCreate(UserBase):
    password: str = Field(..., example="contraseñaSegura")


class UserRead(UserBase):
    id: str

    model_config = {
        "from_attributes": True
    }
