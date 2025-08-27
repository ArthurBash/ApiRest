from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str



class TokenData(BaseModel):
    """Schema para datos del token JWT"""
    user_id: int
    username: str = None