"""
Education endpoints for DeFi learning and explanations
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import Optional, Dict, Any

from app.core.database import get_db
from app.core.exceptions import AuthenticationError
from app.services.auth_service import AuthService
from app.services.education_service import EducationService

router = APIRouter()
security = HTTPBearer()


class EducationRequest(BaseModel):
    """Education request model"""
    topic: str
    level: Optional[str] = "beginner"  # beginner, intermediate, advanced
    context: Optional[str] = None


class EducationResponse(BaseModel):
    """Education response model"""
    topic: str
    level: str
    explanation: str
    key_concepts: list
    examples: list
    related_topics: list
    resources: list


@router.get("/{topic}", response_model=EducationResponse)
async def get_education_content(
    topic: str,
    level: str = "beginner",
    context: Optional[str] = None,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    """Get educational content about a DeFi topic"""
    auth_service = AuthService(db)
    education_service = EducationService(db)
    
    # Get current user
    user = await auth_service.get_current_user(credentials.credentials)
    
    # Get education content
    content = await education_service.get_education_content(
        topic=topic,
        level=level,
        context=context
    )
    
    return EducationResponse(
        topic=content["topic"],
        level=content["level"],
        explanation=content["explanation"],
        key_concepts=content["key_concepts"],
        examples=content["examples"],
        related_topics=content["related_topics"],
        resources=content["resources"]
    )


@router.post("/explain", response_model=EducationResponse)
async def explain_concept(
    request: EducationRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    """Get AI-powered explanation of a DeFi concept"""
    auth_service = AuthService(db)
    education_service = EducationService(db)
    
    # Get current user
    user = await auth_service.get_current_user(credentials.credentials)
    
    # Get explanation
    explanation = await education_service.explain_concept(
        topic=request.topic,
        level=request.level,
        context=request.context
    )
    
    return EducationResponse(
        topic=explanation["topic"],
        level=explanation["level"],
        explanation=explanation["explanation"],
        key_concepts=explanation["key_concepts"],
        examples=explanation["examples"],
        related_topics=explanation["related_topics"],
        resources=explanation["resources"]
    )


@router.get("/topics/list")
async def list_education_topics(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    """Get list of available education topics"""
    auth_service = AuthService(db)
    education_service = EducationService(db)
    
    # Get current user
    user = await auth_service.get_current_user(credentials.credentials)
    
    # Get topics list
    topics = await education_service.get_available_topics()
    
    return {"topics": topics}
