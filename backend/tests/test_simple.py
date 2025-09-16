"""
Simple tests to verify basic functionality
"""

import pytest
import asyncio
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
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test_simple.db"

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


@pytest.fixture(scope="function")
async def db_session():
    """Create a test database session."""
    # Create tables
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Create session
    async with TestSessionLocal() as session:
        yield session
        await session.rollback()
        await session.close()
    
    # Drop tables
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client with database session override."""
    async def override_get_db():
        yield db_session
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()


class TestSimpleAuth:
    """Simple authentication tests."""
    
    @pytest.mark.asyncio
    async def test_create_user_simple(self, db_session):
        """Test user creation with simple approach."""
        auth_service = AuthService(db_session)
        user = await auth_service.create_user(
            email="test@example.com",
            password="password123"
        )
        assert user.email == "test@example.com"
        assert user.hashed_password != "password123"
        assert user.is_active is True
    
    @pytest.mark.asyncio
    async def test_authenticate_user_simple(self, db_session):
        """Test user authentication with simple approach."""
        auth_service = AuthService(db_session)
        
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
    
    def test_password_hashing_simple(self):
        """Test password hashing."""
        auth_service = AuthService(None)
        password = "testpassword123"
        hashed = auth_service.get_password_hash(password)
        assert hashed != password
        assert auth_service.verify_password(password, hashed) is True
        assert auth_service.verify_password("wrongpassword", hashed) is False
    
    def test_token_creation_simple(self):
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


class TestSimpleEndpoints:
    """Simple endpoint tests."""
    
    def test_health_check_simple(self, client):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"
    
    def test_signup_simple(self, client):
        """Test user signup endpoint."""
        response = client.post(
            "/api/v1/auth/signup",
            json={
                "email": "newuser@example.com",
                "password": "securepassword123"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "newuser@example.com"
        assert "id" in data
        assert data["is_active"] is True
