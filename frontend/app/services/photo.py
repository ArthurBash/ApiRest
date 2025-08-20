import requests


import os
from typing import Optional, Dict, Any
from flask import current_app

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
