"""
Authentication endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, EmailStr
from typing import Optional
from jose import jwt
from datetime import datetime, timedelta

from app.core.database import get_db
from app.core.config import settings
from app.core.exceptions import AuthenticationError
from app.models.user import User
from app.services.auth_service import AuthService

router = APIRouter()
security = HTTPBearer()


class UserSignup(BaseModel):
    """User signup request model"""
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    """User login request model"""
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Token response model"""
    access_token: str
    token_type: str
    expires_in: int


class UserResponse(BaseModel):
    """User response model"""
    id: str
    email: str
    is_active: bool
    is_verified: bool
    created_at: datetime


@router.post("/signup", response_model=UserResponse)
async def signup(
    user_data: UserSignup,
    db: AsyncSession = Depends(get_db)
):
    """Register a new user"""
    auth_service = AuthService(db)
    
    # Check if user already exists
    existing_user = await auth_service.get_user_by_email(user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    user = await auth_service.create_user(
        email=user_data.email,
        password=user_data.password
    )
    
    return UserResponse(
        id=str(user.id),
        email=user.email,
        is_active=user.is_active,
        is_verified=user.is_verified,
        created_at=user.created_at
    )


@router.post("/login", response_model=TokenResponse)
async def login(
    login_data: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    """Authenticate user and return access token"""
    auth_service = AuthService(db)
    
    # Authenticate user
    user = await auth_service.authenticate_user(
        email=login_data.email,
        password=login_data.password
    )
    
    if not user:
        raise AuthenticationError("Invalid email or password")
    
    if not user.is_active:
        raise AuthenticationError("Account is deactivated")
    
    # Generate access token
    access_token = auth_service.create_access_token(user.id)
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    """Get current authenticated user"""
    auth_service = AuthService(db)
    
    # Verify token and get user
    user = await auth_service.get_current_user(credentials.credentials)
    
    return UserResponse(
        id=str(user.id),
        email=user.email,
        is_active=user.is_active,
        is_verified=user.is_verified,
        created_at=user.created_at
    )


@router.post("/logout")
async def logout():
    """Logout user (client-side token removal)"""
    return {"message": "Successfully logged out"}
