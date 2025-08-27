import time
from typing import Dict
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from app.exceptions import RateLimitError


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, calls: int = 5, period: int = 60):
        super().__init__(app)
        self.calls = calls  # Número máximo de llamadas
        self.period = period  # Período en segundos
        self.requests: Dict[str, list] = {}

    def _get_client_ip(self, request: Request) -> str:
        """Obtener IP del cliente"""
        # Revisar headers de proxy primero
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip
        
        # IP directa del cliente
        return request.client.host if request.client else "unknown"

    def _is_rate_limited(self, client_ip: str, path: str) -> tuple[bool, int]:
        """Verificar si el cliente está limitado por rate limit"""
        current_time = time.time()
        key = f"{client_ip}:{path}"
        
        # Limpiar requests antiguos
        if key in self.requests:
            self.requests[key] = [
                req_time for req_time in self.requests[key]
                if current_time - req_time < self.period
            ]
        else:
            self.requests[key] = []
        
        # Verificar límite
        if len(self.requests[key]) >= self.calls:
            oldest_request = min(self.requests[key])
            retry_after = int(self.period - (current_time - oldest_request))
            return True, retry_after
        
        # Agregar request actual
        self.requests[key].append(current_time)
        return False, 0

    async def dispatch(self, request: Request, call_next):
        # Solo aplicar rate limit a endpoints de login
        if request.url.path.endswith("/token/login"):
            client_ip = self._get_client_ip(request)
            is_limited, retry_after = self._is_rate_limited(client_ip, request.url.path)
            
            if is_limited:
                raise RateLimitError()
        
        response = await call_next(request)
        return response