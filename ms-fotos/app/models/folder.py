from app.db.base import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class Folder(Base):
    __tablename__ = "folders"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    path = Column(String(512), nullable=False)
    date_created = Column(DateTime, server_default=func.now(), nullable=False)
    is_active = Column(Boolean, default=True)
    
    # Relación
    photos = relationship("Photo", back_populates="folder")
    
    def __str__(self) -> str:
        return f"Carpeta: {self.name} - Path: {self.path}"