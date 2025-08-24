from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class Photo(Base):
    __tablename__ = "photos"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    path = Column(String(512), unique=True, nullable=False)
    user_id = Column(Integer, nullable=False)
    folder_id = Column(Integer, ForeignKey("folders.id"), nullable=False)
    date = Column(DateTime, server_default=func.now(), nullable=False)
    is_active = Column(Boolean, default=True)
    
    # Relación
    folder = relationship("Folder", back_populates="photos")

    def __str__(self) -> str:
        return f"nombre {self.name} {self.path}"