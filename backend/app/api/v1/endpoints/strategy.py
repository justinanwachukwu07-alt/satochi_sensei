"""
Strategy recommendation and execution endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uuid

from app.core.database import get_db
from app.core.exceptions import AuthenticationError, NotFoundError
from app.models.user import User
from app.models.recommendation import Recommendation
from app.services.auth_service import AuthService
from app.services.strategy_service import StrategyService

router = APIRouter()
security = HTTPBearer()


class StrategyRecommendationRequest(BaseModel):
    """Strategy recommendation request model"""
    risk_tolerance: Optional[str] = "medium"  # low, medium, high
    investment_amount: Optional[float] = None
    time_horizon: Optional[str] = "medium"  # short, medium, long
    preferred_protocols: Optional[List[str]] = None


class StrategyExecutionRequest(BaseModel):
    """Strategy execution request model"""
    recommendation_id: str
    transaction_signature: str
    gas_fee: Optional[float] = None


class RecommendationResponse(BaseModel):
    """Recommendation response model"""
    id: str
    strategy_type: str
    risk_score: float
    expected_apy: Optional[float]
    explanation: Optional[str]
    status: str
    created_at: str
    raw_input: Dict[str, Any]
    ai_output: Dict[str, Any]


class ExecutionResponse(BaseModel):
    """Execution response model"""
    transaction_hash: str
    status: str
    estimated_confirmation_time: Optional[str]
    gas_used: Optional[float]


@router.post("/recommend", response_model=RecommendationResponse)
async def get_strategy_recommendation(
    request: StrategyRecommendationRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    """Get AI-powered DeFi strategy recommendations"""
    auth_service = AuthService(db)
    strategy_service = StrategyService(db)
    
    # Get current user
    user = await auth_service.get_current_user(credentials.credentials)
    
    # Generate strategy recommendation
    recommendation = await strategy_service.generate_recommendation(
        user_id=user.id,
        risk_tolerance=request.risk_tolerance,
        investment_amount=request.investment_amount,
        time_horizon=request.time_horizon,
        preferred_protocols=request.preferred_protocols
    )
    
    return RecommendationResponse(
        id=str(recommendation.id),
        strategy_type=recommendation.strategy_type,
        risk_score=recommendation.risk_score,
        expected_apy=recommendation.expected_apy,
        explanation=recommendation.explanation,
        status=recommendation.status,
        created_at=recommendation.created_at.isoformat(),
        raw_input=recommendation.raw_input,
        ai_output=recommendation.ai_output
    )


@router.get("/recommendations", response_model=List[RecommendationResponse])
async def get_user_recommendations(
    limit: int = 10,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    """Get user's strategy recommendations history"""
    auth_service = AuthService(db)
    strategy_service = StrategyService(db)
    
    # Get current user
    user = await auth_service.get_current_user(credentials.credentials)
    
    # Get user recommendations
    recommendations = await strategy_service.get_user_recommendations(
        user_id=user.id,
        limit=limit
    )
    
    return [
        RecommendationResponse(
            id=str(rec.id),
            strategy_type=rec.strategy_type,
            risk_score=rec.risk_score,
            expected_apy=rec.expected_apy,
            explanation=rec.explanation,
            status=rec.status,
            created_at=rec.created_at.isoformat(),
            raw_input=rec.raw_input,
            ai_output=rec.ai_output
        )
        for rec in recommendations
    ]


@router.get("/recommendations/{recommendation_id}", response_model=RecommendationResponse)
async def get_recommendation(
    recommendation_id: str,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    """Get a specific recommendation by ID"""
    auth_service = AuthService(db)
    strategy_service = StrategyService(db)
    
    # Get current user
    user = await auth_service.get_current_user(credentials.credentials)
    
    # Get recommendation
    recommendation = await strategy_service.get_recommendation_by_id(
        uuid.UUID(recommendation_id)
    )
    
    if not recommendation:
        raise NotFoundError("Recommendation not found")
    
    if recommendation.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    return RecommendationResponse(
        id=str(recommendation.id),
        strategy_type=recommendation.strategy_type,
        risk_score=recommendation.risk_score,
        expected_apy=recommendation.expected_apy,
        explanation=recommendation.explanation,
        status=recommendation.status,
        created_at=recommendation.created_at.isoformat(),
        raw_input=recommendation.raw_input,
        ai_output=recommendation.ai_output
    )


@router.post("/execute", response_model=ExecutionResponse)
async def execute_strategy(
    request: StrategyExecutionRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    """Execute a recommended strategy"""
    auth_service = AuthService(db)
    strategy_service = StrategyService(db)
    
    # Get current user
    user = await auth_service.get_current_user(credentials.credentials)
    
    # Get recommendation
    recommendation = await strategy_service.get_recommendation_by_id(
        uuid.UUID(request.recommendation_id)
    )
    
    if not recommendation:
        raise NotFoundError("Recommendation not found")
    
    if recommendation.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    # Execute strategy
    execution_result = await strategy_service.execute_strategy(
        recommendation=recommendation,
        transaction_signature=request.transaction_signature,
        gas_fee=request.gas_fee
    )
    
    return ExecutionResponse(
        transaction_hash=execution_result["transaction_hash"],
        status=execution_result["status"],
        estimated_confirmation_time=execution_result.get("estimated_confirmation_time"),
        gas_used=execution_result.get("gas_used")
    )
