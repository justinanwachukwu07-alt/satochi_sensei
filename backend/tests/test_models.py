"""
Database models tests
"""

import pytest
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
from datetime import datetime

from app.models.user import User
from app.models.wallet import Wallet, NetworkType
from app.models.recommendation import Recommendation


@pytest.mark.unit
class TestUserModel:
    """Test User model."""
    
    @pytest.mark.asyncio
    async def test_create_user(self, db_session: AsyncSession):
        """Test user creation."""
        user = User(
            email="test@example.com",
            hashed_password="hashed_password_123"
        )
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)
        
        assert user.id is not None
        assert user.email == "test@example.com"
        assert user.hashed_password == "hashed_password_123"
        assert user.is_active is True
        assert user.is_verified is False
        assert user.created_at is not None
        assert isinstance(user.id, str)
    
    @pytest.mark.asyncio
    async def test_user_repr(self, db_session: AsyncSession):
        """Test user string representation."""
        user = User(
            email="test@example.com",
            hashed_password="hashed_password_123"
        )
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)
        
        repr_str = repr(user)
        assert "User" in repr_str
        assert str(user.id) in repr_str
        assert user.email in repr_str
    
    @pytest.mark.asyncio
    async def test_user_relationships(self, db_session: AsyncSession):
        """Test user relationships."""
        user = User(
            email="test@example.com",
            hashed_password="hashed_password_123"
        )
        db_session.add(user)
        await db_session.commit()
        await db_session.refresh(user)
        
        # Test wallets relationship
        wallet = Wallet(
            user_id=user.id,
            address="SP2J6ZY48GV1EZ5V2V5RB9MP66SW86PYKKNRV9EJ7",
            network=NetworkType.STACKS,
            label="Test Wallet"
        )
        db_session.add(wallet)
        await db_session.commit()
        
        # Test recommendations relationship
        recommendation = Recommendation(
            user_id=user.id,
            raw_input={"test": "data"},
            ai_output={"strategy": "test"},
            strategy_type="liquidity_provision",
            risk_score=0.7,
            expected_apy=12.5,
            explanation="Test explanation",
            status="pending"
        )
        db_session.add(recommendation)
        await db_session.commit()
        
        # Refresh user to get relationships
        await db_session.refresh(user)
        
        assert len(user.wallets) == 1
        assert len(user.recommendations) == 1
        assert user.wallets[0].address == "SP2J6ZY48GV1EZ5V2V5RB9MP66SW86PYKKNRV9EJ7"
        assert user.recommendations[0].strategy_type == "liquidity_provision"


@pytest.mark.unit
class TestWalletModel:
    """Test Wallet model."""
    
    @pytest.mark.asyncio
    async def test_create_wallet(self, db_session: AsyncSession, test_user: User):
        """Test wallet creation."""
        wallet = Wallet(
            user_id=test_user.id,
            address="SP2J6ZY48GV1EZ5V2V5RB9MP66SW86PYKKNRV9EJ7",
            network=NetworkType.STACKS,
            label="Test Wallet"
        )
        db_session.add(wallet)
        await db_session.commit()
        await db_session.refresh(wallet)
        
        assert wallet.id is not None
        assert wallet.user_id == test_user.id
        assert wallet.address == "SP2J6ZY48GV1EZ5V2V5RB9MP66SW86PYKKNRV9EJ7"
        assert wallet.network == NetworkType.STACKS
        assert wallet.label == "Test Wallet"
        assert wallet.is_active is True
        assert wallet.created_at is not None
        assert isinstance(wallet.id, str)
    
    @pytest.mark.asyncio
    async def test_wallet_repr(self, db_session: AsyncSession, test_user: User):
        """Test wallet string representation."""
        wallet = Wallet(
            user_id=test_user.id,
            address="SP2J6ZY48GV1EZ5V2V5RB9MP66SW86PYKKNRV9EJ7",
            network=NetworkType.STACKS,
            label="Test Wallet"
        )
        db_session.add(wallet)
        await db_session.commit()
        await db_session.refresh(wallet)
        
        repr_str = repr(wallet)
        assert "Wallet" in repr_str
        assert str(wallet.id) in repr_str
        assert wallet.address in repr_str
        assert wallet.network.value in repr_str
    
    @pytest.mark.asyncio
    async def test_wallet_network_types(self, db_session: AsyncSession, test_user: User):
        """Test wallet with different network types."""
        # Test Stacks wallet
        stacks_wallet = Wallet(
            user_id=test_user.id,
            address="SP2J6ZY48GV1EZ5V2V5RB9MP66SW86PYKKNRV9EJ7",
            network=NetworkType.STACKS,
            label="Stacks Wallet"
        )
        db_session.add(stacks_wallet)
        
        # Test Bitcoin wallet
        bitcoin_wallet = Wallet(
            user_id=test_user.id,
            address="1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
            network=NetworkType.BITCOIN,
            label="Bitcoin Wallet"
        )
        db_session.add(bitcoin_wallet)
        
        await db_session.commit()
        
        assert stacks_wallet.network == NetworkType.STACKS
        assert bitcoin_wallet.network == NetworkType.BITCOIN
    
    @pytest.mark.asyncio
    async def test_wallet_user_relationship(self, db_session: AsyncSession, test_user: User):
        """Test wallet-user relationship."""
        wallet = Wallet(
            user_id=test_user.id,
            address="SP2J6ZY48GV1EZ5V2V5RB9MP66SW86PYKKNRV9EJ7",
            network=NetworkType.STACKS,
            label="Test Wallet"
        )
        db_session.add(wallet)
        await db_session.commit()
        await db_session.refresh(wallet)
        
        assert wallet.user.id == test_user.id
        assert wallet.user.email == test_user.email


@pytest.mark.unit
class TestRecommendationModel:
    """Test Recommendation model."""
    
    @pytest.mark.asyncio
    async def test_create_recommendation(self, db_session: AsyncSession, test_user: User):
        """Test recommendation creation."""
        recommendation = Recommendation(
            user_id=test_user.id,
            raw_input={"wallet_balance": 1000, "risk_tolerance": "medium"},
            ai_output={"strategy": "liquidity_provision", "protocol": "alex"},
            strategy_type="liquidity_provision",
            risk_score=0.7,
            expected_apy=12.5,
            explanation="This is a test strategy recommendation",
            status="pending"
        )
        db_session.add(recommendation)
        await db_session.commit()
        await db_session.refresh(recommendation)
        
        assert recommendation.id is not None
        assert recommendation.user_id == test_user.id
        assert recommendation.raw_input == {"wallet_balance": 1000, "risk_tolerance": "medium"}
        assert recommendation.ai_output == {"strategy": "liquidity_provision", "protocol": "alex"}
        assert recommendation.strategy_type == "liquidity_provision"
        assert recommendation.risk_score == 0.7
        assert recommendation.expected_apy == 12.5
        assert recommendation.explanation == "This is a test strategy recommendation"
        assert recommendation.status == "pending"
        assert recommendation.executed_at is None
        assert recommendation.transaction_hash is None
        assert recommendation.created_at is not None
        assert isinstance(recommendation.id, str)
    
    @pytest.mark.asyncio
    async def test_recommendation_repr(self, db_session: AsyncSession, test_user: User):
        """Test recommendation string representation."""
        recommendation = Recommendation(
            user_id=test_user.id,
            raw_input={"test": "data"},
            ai_output={"strategy": "test"},
            strategy_type="liquidity_provision",
            risk_score=0.7,
            expected_apy=12.5,
            explanation="Test explanation",
            status="pending"
        )
        db_session.add(recommendation)
        await db_session.commit()
        await db_session.refresh(recommendation)
        
        repr_str = repr(recommendation)
        assert "Recommendation" in repr_str
        assert str(recommendation.id) in repr_str
        assert recommendation.strategy_type in repr_str
        assert str(recommendation.risk_score) in repr_str
    
    @pytest.mark.asyncio
    async def test_recommendation_status_updates(self, db_session: AsyncSession, test_user: User):
        """Test recommendation status updates."""
        recommendation = Recommendation(
            user_id=test_user.id,
            raw_input={"test": "data"},
            ai_output={"strategy": "test"},
            strategy_type="liquidity_provision",
            risk_score=0.7,
            expected_apy=12.5,
            explanation="Test explanation",
            status="pending"
        )
        db_session.add(recommendation)
        await db_session.commit()
        await db_session.refresh(recommendation)
        
        # Update status to executed
        recommendation.status = "executed"
        recommendation.executed_at = datetime.utcnow()
        recommendation.transaction_hash = "0x1234567890abcdef"
        
        await db_session.commit()
        await db_session.refresh(recommendation)
        
        assert recommendation.status == "executed"
        assert recommendation.executed_at is not None
        assert recommendation.transaction_hash == "0x1234567890abcdef"
    
    @pytest.mark.asyncio
    async def test_recommendation_user_relationship(self, db_session: AsyncSession, test_user: User):
        """Test recommendation-user relationship."""
        recommendation = Recommendation(
            user_id=test_user.id,
            raw_input={"test": "data"},
            ai_output={"strategy": "test"},
            strategy_type="liquidity_provision",
            risk_score=0.7,
            expected_apy=12.5,
            explanation="Test explanation",
            status="pending"
        )
        db_session.add(recommendation)
        await db_session.commit()
        await db_session.refresh(recommendation)
        
        assert recommendation.user.id == test_user.id
        assert recommendation.user.email == test_user.email
    
    @pytest.mark.asyncio
    async def test_recommendation_with_optional_fields(self, db_session: AsyncSession, test_user: User):
        """Test recommendation with optional fields."""
        recommendation = Recommendation(
            user_id=test_user.id,
            raw_input={"test": "data"},
            ai_output={"strategy": "test"},
            strategy_type="yield_farming",
            risk_score=0.8,
            expected_apy=None,  # Optional field
            explanation=None,   # Optional field
            status="pending"
        )
        db_session.add(recommendation)
        await db_session.commit()
        await db_session.refresh(recommendation)
        
        assert recommendation.expected_apy is None
        assert recommendation.explanation is None
        assert recommendation.strategy_type == "yield_farming"
        assert recommendation.risk_score == 0.8
