from pydantic import BaseModel
from typing import List, TypeVar, Generic

T = TypeVar('T')


class SuccessResponse(BaseModel):
    """Schema para respuestas de éxito"""
    message: str
    success: bool = True


class ErrorResponse(BaseModel):
    """Schema para respuestas de error"""
    detail: str
    success: bool = False


class PaginatedResponse(BaseModel, Generic[T]):
    """Schema genérico para respuestas paginadas"""
    items: List[T]
    total: int
    skip: int
    limit: int
    has_next: bool
    has_previous: bool
