"""
Pytest configuration and fixtures
"""

import pytest
import asyncio
from typing import AsyncGenerator, Generator
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from httpx import AsyncClient
import tempfile
import os

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
from app.core.database import get_db, Base
from app.core.config import settings
from app.models.user import User
from app.models.wallet import Wallet, NetworkType
from app.models.recommendation import Recommendation
from app.services.auth_service import AuthService


# Test database URL
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test_satoshi_sensei.db"

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


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Create a test database session."""
    # Create tables
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Create session
    async with TestSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
    
    # Drop tables
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
def client(db_session: AsyncSession) -> TestClient:
    """Create a test client with database session override."""
    async def override_get_db():
        yield db_session
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
async def async_client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Create an async test client."""
    def override_get_db():
        return db_session
    
    app.dependency_overrides[get_db] = override_get_db
    
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
    
    app.dependency_overrides.clear()


@pytest.fixture
async def test_user(db_session: AsyncSession) -> User:
    """Create a test user."""
    auth_service = AuthService(db_session)
    user = await auth_service.create_user(
        email="test@example.com",
        password="testpassword123"
    )
    return user


@pytest.fixture
async def test_user_token(test_user: User) -> str:
    """Create a JWT token for test user."""
    auth_service = AuthService(None)  # We don't need db for token creation
    token = auth_service.create_access_token(test_user.id)
    return token


@pytest.fixture
async def test_wallet(db_session: AsyncSession, test_user: User) -> Wallet:
    """Create a test wallet."""
    wallet = Wallet(
        user_id=test_user.id,
        address="SP2J6ZY48GV1EZ5V2V5RB9MP66SW86PYKKNRV9EJ7",
        network=NetworkType.STACKS,
        label="Test Wallet"
    )
    db_session.add(wallet)
    await db_session.commit()
    await db_session.refresh(wallet)
    return wallet


@pytest.fixture
async def test_recommendation(db_session: AsyncSession, test_user: User) -> Recommendation:
    """Create a test recommendation."""
    recommendation = Recommendation(
        user_id=test_user.id,
        raw_input={"test": "data"},
        ai_output={"strategy": "test"},
        strategy_type="liquidity_provision",
        risk_score=0.7,
        expected_apy=12.5,
        explanation="Test strategy explanation",
        status="pending"
    )
    db_session.add(recommendation)
    await db_session.commit()
    await db_session.refresh(recommendation)
    return recommendation


@pytest.fixture
def auth_headers(test_user_token: str) -> dict:
    """Create authorization headers."""
    return {"Authorization": f"Bearer {test_user_token}"}


@pytest.fixture
def sample_wallet_data() -> dict:
    """Sample wallet connection data."""
    return {
        "address": "SP2J6ZY48GV1EZ5V2V5RB9MP66SW86PYKKNRV9EJ7",
        "network": "stacks",
        "label": "Test Wallet"
    }


@pytest.fixture
def sample_strategy_request() -> dict:
    """Sample strategy recommendation request."""
    return {
        "risk_tolerance": "medium",
        "investment_amount": 1000.0,
        "time_horizon": "long",
        "preferred_protocols": ["alex", "arkadiko"]
    }


@pytest.fixture
def sample_education_request() -> dict:
    """Sample education request."""
    return {
        "topic": "liquidity_provision",
        "level": "beginner",
        "context": "I want to learn about providing liquidity"
    }
