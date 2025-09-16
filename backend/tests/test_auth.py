"""
Authentication tests
"""

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from unittest.mock import patch, AsyncMock
import uuid

from app.models.user import User
from app.services.auth_service import AuthService


@pytest.mark.auth
class TestAuthEndpoints:
    """Test authentication endpoints."""
    
    @pytest.mark.asyncio
    async def test_signup_success(self, client: TestClient):
        """Test successful user signup."""
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
        assert data["is_verified"] is False
    
    def test_signup_duplicate_email(self, client: TestClient, test_user: User):
        """Test signup with duplicate email."""
        response = client.post(
            "/api/v1/auth/signup",
            json={
                "email": "test@example.com",
                "password": "password123"
            }
        )
        assert response.status_code == 400
        assert "Email already registered" in response.json()["detail"]
    
    def test_signup_invalid_email(self, client: TestClient):
        """Test signup with invalid email."""
        response = client.post(
            "/api/v1/auth/signup",
            json={
                "email": "invalid-email",
                "password": "password123"
            }
        )
        assert response.status_code == 422
    
    def test_login_success(self, client: TestClient, test_user: User):
        """Test successful login."""
        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "test@example.com",
                "password": "testpassword123"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert "expires_in" in data
    
    def test_login_invalid_credentials(self, client: TestClient):
        """Test login with invalid credentials."""
        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "test@example.com",
                "password": "wrongpassword"
            }
        )
        assert response.status_code == 401
        assert "Invalid email or password" in response.json()["detail"]
    
    def test_login_nonexistent_user(self, client: TestClient):
        """Test login with nonexistent user."""
        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "nonexistent@example.com",
                "password": "password123"
            }
        )
        assert response.status_code == 401
    
    def test_get_current_user_success(self, client: TestClient, auth_headers: dict, test_user: User):
        """Test getting current user with valid token."""
        response = client.get("/api/v1/auth/me", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == test_user.email
        assert data["id"] == str(test_user.id)
    
    def test_get_current_user_invalid_token(self, client: TestClient):
        """Test getting current user with invalid token."""
        response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": "Bearer invalid_token"}
        )
        assert response.status_code == 401
    
    def test_get_current_user_no_token(self, client: TestClient):
        """Test getting current user without token."""
        response = client.get("/api/v1/auth/me")
        assert response.status_code == 403
    
    def test_logout(self, client: TestClient):
        """Test logout endpoint."""
        response = client.post("/api/v1/auth/logout")
        assert response.status_code == 200
        assert response.json()["message"] == "Successfully logged out"


@pytest.mark.auth
class TestAuthService:
    """Test authentication service."""
    
    @pytest.mark.asyncio
    async def test_create_user(self, db_session):
        """Test user creation."""
        auth_service = AuthService(db_session)
        user = await auth_service.create_user(
            email="newuser@example.com",
            password="password123"
        )
        assert user.email == "newuser@example.com"
        assert user.hashed_password != "password123"  # Should be hashed
        assert user.is_active is True
        assert user.is_verified is False
    
    @pytest.mark.asyncio
    async def test_get_user_by_email(self, db_session, test_user: User):
        """Test getting user by email."""
        auth_service = AuthService(db_session)
        user = await auth_service.get_user_by_email("test@example.com")
        assert user is not None
        assert user.email == test_user.email
    
    @pytest.mark.asyncio
    async def test_get_user_by_email_not_found(self, db_session):
        """Test getting user by email when not found."""
        auth_service = AuthService(db_session)
        user = await auth_service.get_user_by_email("nonexistent@example.com")
        assert user is None
    
    @pytest.mark.asyncio
    async def test_get_user_by_id(self, db_session, test_user: User):
        """Test getting user by ID."""
        auth_service = AuthService(db_session)
        user = await auth_service.get_user_by_id(test_user.id)
        assert user is not None
        assert user.id == test_user.id
    
    @pytest.mark.asyncio
    async def test_authenticate_user_success(self, db_session, test_user: User):
        """Test successful user authentication."""
        auth_service = AuthService(db_session)
        user = await auth_service.authenticate_user(
            "test@example.com",
            "testpassword123"
        )
        assert user is not None
        assert user.email == test_user.email
    
    @pytest.mark.asyncio
    async def test_authenticate_user_wrong_password(self, db_session, test_user: User):
        """Test authentication with wrong password."""
        auth_service = AuthService(db_session)
        user = await auth_service.authenticate_user(
            "test@example.com",
            "wrongpassword"
        )
        assert user is None
    
    @pytest.mark.asyncio
    async def test_authenticate_user_nonexistent(self, db_session):
        """Test authentication with nonexistent user."""
        auth_service = AuthService(db_session)
        user = await auth_service.authenticate_user(
            "nonexistent@example.com",
            "password123"
        )
        assert user is None
    
    def test_create_access_token(self, test_user: User):
        """Test JWT token creation."""
        auth_service = AuthService(None)
        token = auth_service.create_access_token(test_user.id)
        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0
    
    def test_verify_token_valid(self, test_user: User):
        """Test token verification with valid token."""
        auth_service = AuthService(None)
        token = auth_service.create_access_token(test_user.id)
        user_id = auth_service.verify_token(token)
        assert user_id == str(test_user.id)
    
    def test_verify_token_invalid(self):
        """Test token verification with invalid token."""
        auth_service = AuthService(None)
        user_id = auth_service.verify_token("invalid_token")
        assert user_id is None
    
    @pytest.mark.asyncio
    async def test_get_current_user_success(self, db_session, test_user: User):
        """Test getting current user from token."""
        auth_service = AuthService(db_session)
        token = auth_service.create_access_token(test_user.id)
        user = await auth_service.get_current_user(token)
        assert user.id == test_user.id
        assert user.email == test_user.email
    
    @pytest.mark.asyncio
    async def test_get_current_user_invalid_token(self, db_session):
        """Test getting current user with invalid token."""
        auth_service = AuthService(db_session)
        with pytest.raises(Exception):  # Should raise AuthenticationError
            await auth_service.get_current_user("invalid_token")
    
    def test_password_hashing(self):
        """Test password hashing and verification."""
        auth_service = AuthService(None)
        password = "testpassword123"
        hashed = auth_service.get_password_hash(password)
        assert hashed != password
        assert auth_service.verify_password(password, hashed) is True
        assert auth_service.verify_password("wrongpassword", hashed) is False
