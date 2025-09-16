"""
Wallet model for managing connected wallets
"""

from sqlalchemy import Column, String, DateTime, ForeignKey, Enum, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
import enum

from app.core.database import Base


class NetworkType(str, enum.Enum):
    """Supported blockchain networks"""
    STACKS = "stacks"
    BITCOIN = "bitcoin"


class Wallet(Base):
    """Wallet model for connected blockchain wallets"""
    
    __tablename__ = "wallets"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    address = Column(String(255), nullable=False, index=True)
    network = Column(Enum(NetworkType), nullable=False)
    label = Column(String(100), nullable=True)  # User-defined wallet label
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="wallets")
    
    def __repr__(self):
        return f"<Wallet(id={self.id}, address={self.address}, network={self.network})>"
