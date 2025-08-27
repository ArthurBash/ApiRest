import argon2
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError


class PasswordUtils:
    def __init__(self):

        self.ph = PasswordHasher(
            time_cost=2,      # Iteraciones
            memory_cost=65536, # Memoria en KB (64MB)
            parallelism=1,    # Threads
            hash_len=32,      # Longitud del hash
            salt_len=16,      # Longitud del salt
            encoding='utf-8'
        )

    def hash_password(self, password: str) -> str:
        """Hash de contraseña usando Argon2id"""
        return self.ph.hash(password)

    def verify_password(self, password: str, hashed_password: str) -> bool:
        """Verificar contraseña contra hash"""
        try:
            self.ph.verify(hashed_password, password)
            return True
        except VerifyMismatchError:
            return False