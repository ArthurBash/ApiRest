from typing import List
from services.folder_service import FolderService
from schemas.folder_schemas import FolderCreate, FolderUpdate, FolderResponse
from schemas.common_schemas import SuccessResponse
from exceptions import FolderNotFoundError, DecodingError, ValidationError, BaseCustomException


class FolderController:
    def __init__(self, folder_service: FolderService):
        self.folder_service = folder_service

    def create_folder(self, folder_data: FolderCreate) -> FolderResponse:
        """Crear nueva carpeta"""
        try:
            return self.folder_service.create_folder(folder_data)
        except BaseCustomException:
            # deja pasar excepciones de dominio
            raise
        except Exception as e:
            # cualquier otra excepción se convierte en BaseCustomException
            raise BaseCustomException(message="Error interno al crear carpeta", original_exception=str(e))

    def get_folder_by_id(self, folder_id: str) -> FolderResponse:
        """Obtener carpeta por ID"""
        try:
            return self.folder_service.get_folder_by_id(folder_id)
        except BaseCustomException:
            raise
        except Exception as e:
            raise BaseCustomException(message="Error interno al obtener carpeta", original_exception=str(e))

    def get_all_folders(self, skip: int = 0, limit: int = 100) -> List[FolderResponse]:
        """Obtener todas las carpetas"""
        try:
            return self.folder_service.get_all_folders(skip=skip, limit=limit)
        except BaseCustomException:
            raise
        except Exception as e:
            raise BaseCustomException(message="Error interno al listar carpetas", original_exception=str(e))

    def update_folder(self, folder_id: str, folder_data: FolderUpdate) -> FolderResponse:
        """Actualizar carpeta"""
        try:
            return self.folder_service.update_folder(folder_id, folder_data)
        except BaseCustomException:
            raise
        except Exception as e:
            raise BaseCustomException(message="Error interno al actualizar carpeta", original_exception=str(e))

    def delete_folder(self, folder_id: str) -> SuccessResponse:
        """Eliminar carpeta"""
        try:
            self.folder_service.delete_folder(folder_id)
            return SuccessResponse(message="Carpeta eliminada correctamente")
        except BaseCustomException:
            raise
        except Exception as e:
            raise BaseCustomException(message="Error interno al eliminar carpeta", original_exception=str(e))
