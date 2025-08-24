import requests


import os
from typing import Optional, Dict, Any
from flask import current_app,session
import logging


def get_folders_from_api():
    """
    Función que obtiene las carpetas desde la API FastAPI
    """
    try:
        access_token = session.get("access_token")
        if not access_token:
            logging.error("No se encontró token de acceso")
            return []

        # URL de tu API FastAPI
        api_url = "http://ms-fotos/api/photo/folders"  
        
        # Headers con autenticación
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        params = {
            "skip": 0,
            "limit": 100  
        }
        
        # Hace la petición
        response = requests.get(api_url, headers=headers, params=params, timeout=10)
        
        if response.status_code == 200:
            folders_data = response.json()
            
            folders = []
            for folder in folders_data:
                folders.append({
                    "id": folder["id"],          
                    "name": folder["name"],     
                    "path": folder.get("path", ""),
                    "is_active": folder.get("is_active", True)
                })
            
            logging.info(f"Se obtuvieron {len(folders)} carpetas desde la API")
            return folders
            
        elif response.status_code == 401:
            logging.error("Token de acceso inválido o expirado")
            return []
        elif response.status_code == 403:
            logging.error("No tienes permisos para acceder a las carpetas")
            return []
        else:
            logging.error(f"Error al obtener carpetas: {response.status_code} - {response.text}")
            return []
            
    except requests.RequestException as e:
        logging.error(f"Error de conexión al obtener carpetas: {e}")
        return []
    except Exception as e:
        logging.error(f"Error inesperado al obtener carpetas: {e}")
        return []

def upload_photo_to_backend(name, user_id, folder_id, token,file):
    headers = {"Authorization": f"Bearer {token}"}

    files = {'file': (file.filename, file.stream, file.mimetype)}
    data = {
        'name': name,
        'user_id': user_id,
        'folder_id': folder_id
    }

    response = requests.post('http://ms-fotos/api/photo/', data=data, files=files, headers=headers)
    return response



class PhotoAPIService:
    """Servicio para comunicarse con el microservicio FastAPI de fotos"""
    
    def __init__(self):
        self.fastapi_base_url = os.getenv("FASTAPI_PHOTO_SERVICE_URL", "http://ms-fotos")
        self.api_prefix = "/api/photo"
    
    def _get_headers(self, token: str) -> Dict[str, str]:
        """Headers comunes para las peticiones"""
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
    
    def get_photos(
        self, 
        token: str, 
        page: int = 1, 
        page_size: int = 20, 
        folder_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Obtiene fotos desde el microservicio FastAPI
        
        Args:
            token: JWT token del usuario
            page: Número de página
            page_size: Cantidad de fotos por página  
            folder_id: ID del folder (opcional)
        
        Returns:
            Dict con fotos y metadatos de paginación
        """
        url = f"{self.fastapi_base_url}{self.api_prefix}/photos"
        
        params = {
            "page": page,
            "page_size": page_size
        }
        
        if folder_id is not None:
            params["folder_id"] = folder_id
        
        try:
            response = requests.get(
                url, 
                headers=self._get_headers(token),
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 401:
                return {"error": "Token expirado o inválido"}
            elif response.status_code == 404:
                return {"error": "Fotos no encontradas"}
            else:
                return {"error": f"Error del servidor: {response.status_code}"}
                
        except requests.exceptions.RequestException as e:
            current_app.logger.error(f"Error comunicándose con FastAPI: {e}")
            return {"error": "Error de conexión con el servicio de fotos"}
    
    def get_single_photo(self, token: str, photo_id: int) -> Dict[str, Any]:
        """Obtiene una foto específica"""
        url = f"{self.fastapi_base_url}{self.api_prefix}/photos/{photo_id}"
        
        try:
            response = requests.get(
                url,
                headers=self._get_headers(token),
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                return {"error": "Foto no encontrada"}
            else:
                return {"error": f"Error: {response.status_code}"}
                
        except requests.exceptions.RequestException as e:
            current_app.logger.error(f"Error obteniendo foto: {e}")
            return {"error": "Error de conexión"}
