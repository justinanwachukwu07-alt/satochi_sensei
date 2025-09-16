"""
Manual tests that handle async sessions directly
"""

import pytest
import asyncio
import uuid
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import tempfile
import os

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
from app.core.database import get_db, Base
from app.models.user import User
from app.services.auth_service import AuthService


# Test database URL
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test_manual.db"

# Create test engine
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
    future=True,
    connect_args={"check_same_thread": False}
)

TestSessionLocal = sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False
)


class TestManualAuth:
    """Manual authentication tests that handle async sessions directly."""
    
    @pytest.mark.asyncio
    async def test_create_user_manual(self):
        """Test user creation with manual session handling."""
        # Create tables
        async with test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        
        # Create session
        async with TestSessionLocal() as session:
            auth_service = AuthService(session)
            user = await auth_service.create_user(
                email="test@example.com",
                password="password123"
            )
            assert user.email == "test@example.com"
            assert user.hashed_password != "password123"
            assert user.is_active is True
        
        # Drop tables
        async with test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
    
    @pytest.mark.asyncio
    async def test_authenticate_user_manual(self):
        """Test user authentication with manual session handling."""
        # Create tables
        async with test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        
        # Create session
        async with TestSessionLocal() as session:
            auth_service = AuthService(session)
            
            # Create user first
            user = await auth_service.create_user(
                email="test@example.com",
                password="password123"
            )
            
            # Test authentication
            authenticated_user = await auth_service.authenticate_user(
                "test@example.com",
                "password123"
            )
            
            assert authenticated_user is not None
            assert authenticated_user.email == "test@example.com"
        
        # Drop tables
        async with test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
    
    def test_password_hashing_manual(self):
        """Test password hashing."""
        auth_service = AuthService(None)
        password = "testpassword123"
        hashed = auth_service.get_password_hash(password)
        assert hashed != password
        assert auth_service.verify_password(password, hashed) is True
        assert auth_service.verify_password("wrongpassword", hashed) is False
    
    def test_token_creation_manual(self):
        """Test JWT token creation."""
        auth_service = AuthService(None)
        user_id = "test-user-id"
        token = auth_service.create_access_token(user_id)
        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0
        
        # Test token verification
        verified_user_id = auth_service.verify_token(token)
        assert verified_user_id == user_id


class TestManualEndpoints:
    """Manual endpoint tests."""
    
    def test_health_check_manual(self):
        """Test health check endpoint."""
        with TestClient(app) as client:
            response = client.get("/health")
            assert response.status_code == 200
            assert response.json()["status"] == "healthy"
    
    def test_signup_manual(self):
        """Test user signup endpoint."""
        with TestClient(app) as client:
            # Use unique email to avoid conflicts
            unique_email = f"manual_test_{uuid.uuid4().hex[:8]}@example.com"
            response = client.post(
                "/api/v1/auth/signup",
                json={
                    "email": unique_email,
                    "password": "securepassword123"
                }
            )
            assert response.status_code == 200
            data = response.json()
            assert data["email"] == unique_email
            assert "id" in data
            assert data["is_active"] is True
