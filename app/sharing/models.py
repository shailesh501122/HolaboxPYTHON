from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.config.database import Base


class Share(Base):
    __tablename__ = "shares"
    
    id = Column(Integer, primary_key=True, index=True)
    share_token = Column(String, unique=True, index=True, nullable=False)
    file_id = Column(Integer, ForeignKey("files.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    password_hash = Column(String, nullable=True)
    expires_at = Column(DateTime, nullable=True)
    
    view_count = Column(Integer, default=0)
    download_count = Column(Integer, default=0)
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    owner = relationship("User", back_populates="shares")
    file = relationship("File", back_populates="shares")
