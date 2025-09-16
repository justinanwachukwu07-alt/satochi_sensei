"""
Recommendation model for AI-generated DeFi strategies
"""

from sqlalchemy import Column, String, DateTime, ForeignKey, Float, Text, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from app.core.database import Base


class Recommendation(Base):
    """AI-generated DeFi strategy recommendations"""
    
    __tablename__ = "recommendations"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    
    # Input data
    raw_input = Column(JSON, nullable=False)  # Wallet balances, market data, etc.
    
    # AI output
    ai_output = Column(JSON, nullable=False)  # Structured AI response
    strategy_type = Column(String(100), nullable=False)  # e.g., "liquidity_provision", "yield_farming"
    risk_score = Column(Float, nullable=False)  # 0.0 to 1.0 risk assessment
    expected_apy = Column(Float, nullable=True)  # Expected annual percentage yield
    
    # Human-readable explanation
    explanation = Column(Text, nullable=True)  # Natural language explanation
    
    # Status tracking
    status = Column(String(50), default="pending")  # pending, executed, cancelled, failed
    executed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="recommendations")
    
    def __repr__(self):
        return f"<Recommendation(id={self.id}, strategy_type={self.strategy_type}, risk_score={self.risk_score})>"
