"""
Strategy management tests
"""

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from unittest.mock import patch, AsyncMock, MagicMock
import uuid
import json

from app.models.recommendation import Recommendation
from app.models.wallet import Wallet
from app.services.strategy_service import StrategyService
from tests.mocks import mock_all_external_apis


@pytest.mark.strategy
class TestStrategyEndpoints:
    """Test strategy management endpoints."""
    
    @patch('app.services.strategy_service.StrategyService.generate_recommendation')
    def test_get_strategy_recommendation_success(self, mock_generate, client: TestClient, auth_headers: dict, sample_strategy_request: dict, test_recommendation: Recommendation):
        """Test successful strategy recommendation."""
        mock_generate.return_value = test_recommendation
        
        response = client.post(
            "/api/v1/strategy/recommend",
            json=sample_strategy_request,
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["strategy_type"] == test_recommendation.strategy_type
        assert data["risk_score"] == test_recommendation.risk_score
        assert data["expected_apy"] == test_recommendation.expected_apy
        assert "id" in data
        assert "created_at" in data
    
    def test_get_strategy_recommendation_unauthorized(self, client: TestClient, sample_strategy_request: dict):
        """Test strategy recommendation without authentication."""
        response = client.post(
            "/api/v1/strategy/recommend",
            json=sample_strategy_request
        )
        assert response.status_code == 403
    
    def test_get_user_recommendations(self, client: TestClient, auth_headers: dict, test_recommendation: Recommendation):
        """Test getting user recommendations."""
        response = client.get("/api/v1/strategy/recommendations", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["id"] == str(test_recommendation.id)
    
    def test_get_user_recommendations_with_limit(self, client: TestClient, auth_headers: dict):
        """Test getting user recommendations with limit."""
        response = client.get("/api/v1/strategy/recommendations?limit=5", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_get_user_recommendations_unauthorized(self, client: TestClient):
        """Test getting recommendations without authentication."""
        response = client.get("/api/v1/strategy/recommendations")
        assert response.status_code == 403
    
    def test_get_recommendation_by_id(self, client: TestClient, auth_headers: dict, test_recommendation: Recommendation):
        """Test getting specific recommendation."""
        response = client.get(
            f"/api/v1/strategy/recommendations/{test_recommendation.id}",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == str(test_recommendation.id)
        assert data["strategy_type"] == test_recommendation.strategy_type
    
    def test_get_recommendation_not_found(self, client: TestClient, auth_headers: dict):
        """Test getting nonexistent recommendation."""
        fake_id = str(uuid.uuid4())
        response = client.get(
            f"/api/v1/strategy/recommendations/{fake_id}",
            headers=auth_headers
        )
        assert response.status_code == 404
    
    def test_get_recommendation_unauthorized(self, client: TestClient, test_recommendation: Recommendation):
        """Test getting recommendation without authentication."""
        response = client.get(f"/api/v1/strategy/recommendations/{test_recommendation.id}")
        assert response.status_code == 403
    
    @patch('app.services.strategy_service.StrategyService.execute_strategy')
    def test_execute_strategy_success(self, mock_execute, client: TestClient, auth_headers: dict, test_recommendation: Recommendation):
        """Test successful strategy execution."""
        mock_execute.return_value = {
            "transaction_hash": "0x1234567890abcdef",
            "status": "pending",
            "estimated_confirmation_time": "2-5 minutes",
            "gas_used": 25000
        }
        
        response = client.post(
            "/api/v1/strategy/execute",
            json={
                "recommendation_id": str(test_recommendation.id),
                "transaction_signature": "0xabcdef1234567890",
                "gas_fee": 25000
            },
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["transaction_hash"] == "0x1234567890abcdef"
        assert data["status"] == "pending"
    
    def test_execute_strategy_not_found(self, client: TestClient, auth_headers: dict):
        """Test executing nonexistent strategy."""
        fake_id = str(uuid.uuid4())
        response = client.post(
            "/api/v1/strategy/execute",
            json={
                "recommendation_id": fake_id,
                "transaction_signature": "0xabcdef1234567890"
            },
            headers=auth_headers
        )
        assert response.status_code == 404
    
    def test_execute_strategy_unauthorized(self, client: TestClient, test_recommendation: Recommendation):
        """Test strategy execution without authentication."""
        response = client.post(
            "/api/v1/strategy/execute",
            json={
                "recommendation_id": str(test_recommendation.id),
                "transaction_signature": "0xabcdef1234567890"
            }
        )
        assert response.status_code == 403


@pytest.mark.strategy
class TestStrategyService:
    """Test strategy service."""
    
    @pytest.mark.asyncio
    @patch('app.services.strategy_service.StrategyService._call_groq_api')
    @patch('app.services.strategy_service.StrategyService._collect_user_data')
    @patch('app.services.strategy_service.StrategyService._get_market_data')
    async def test_generate_recommendation(self, mock_market_data, mock_user_data, mock_groq, db_session, test_user):
        """Test strategy recommendation generation."""
        # Mock dependencies
        mock_user_data.return_value = {"wallets": [], "total_wallets": 0}
        mock_market_data.return_value = {"alex_pools": [], "arkadiko_pools": []}
        mock_groq.return_value = {
            "strategy_type": "liquidity_provision",
            "risk_score": 0.7,
            "expected_apy": 12.5,
            "explanation": "Test strategy",
            "recommendations": []
        }
        
        strategy_service = StrategyService(db_session)
        recommendation = await strategy_service.generate_recommendation(
            user_id=test_user.id,
            risk_tolerance="medium",
            investment_amount=1000.0,
            time_horizon="long"
        )
        
        assert recommendation.user_id == test_user.id
        assert recommendation.strategy_type == "liquidity_provision"
        assert recommendation.risk_score == 0.7
        assert recommendation.expected_apy == 12.5
        assert recommendation.status == "pending"
    
    @pytest.mark.asyncio
    async def test_get_user_recommendations(self, db_session, test_user, test_recommendation: Recommendation):
        """Test getting user recommendations."""
        strategy_service = StrategyService(db_session)
        recommendations = await strategy_service.get_user_recommendations(
            user_id=test_user.id,
            limit=10
        )
        assert len(recommendations) == 1
        assert recommendations[0].id == test_recommendation.id
    
    @pytest.mark.asyncio
    async def test_get_recommendation_by_id(self, db_session, test_recommendation: Recommendation):
        """Test getting recommendation by ID."""
        strategy_service = StrategyService(db_session)
        recommendation = await strategy_service.get_recommendation_by_id(test_recommendation.id)
        assert recommendation is not None
        assert recommendation.id == test_recommendation.id
    
    @pytest.mark.asyncio
    async def test_get_recommendation_by_id_not_found(self, db_session):
        """Test getting recommendation by ID when not found."""
        strategy_service = StrategyService(db_session)
        fake_id = uuid.uuid4()
        recommendation = await strategy_service.get_recommendation_by_id(fake_id)
        assert recommendation is None
    
    @pytest.mark.asyncio
    @patch('httpx.AsyncClient.post')
    async def test_call_groq_api_success(self, mock_post, db_session):
        """Test successful Groq API call."""
        # Mock Groq API response
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{
                "message": {
                    "content": json.dumps({
                        "strategy_type": "yield_farming",
                        "risk_score": 0.6,
                        "expected_apy": 15.0,
                        "explanation": "Test explanation"
                    })
                }
            }]
        }
        mock_post.return_value = mock_response
        
        strategy_service = StrategyService(db_session)
        result = await strategy_service._call_groq_api({"test": "data"})
        
        assert result["strategy_type"] == "yield_farming"
        assert result["risk_score"] == 0.6
        assert result["expected_apy"] == 15.0
    
    @pytest.mark.asyncio
    @patch('httpx.AsyncClient.post')
    async def test_call_groq_api_invalid_json(self, mock_post, db_session):
        """Test Groq API call with invalid JSON response."""
        # Mock Groq API response with non-JSON content
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{
                "message": {
                    "content": "This is not JSON"
                }
            }]
        }
        mock_post.return_value = mock_response
        
        strategy_service = StrategyService(db_session)
        result = await strategy_service._call_groq_api({"test": "data"})
        
        assert result["strategy_type"] == "general_advice"
        assert result["explanation"] == "This is not JSON"
    
    @pytest.mark.asyncio
    @patch('httpx.AsyncClient.post')
    async def test_call_groq_api_error(self, mock_post, db_session):
        """Test Groq API call with error response."""
        # Mock Groq API error response
        mock_response = AsyncMock()
        mock_response.status_code = 500
        mock_post.return_value = mock_response
        
        strategy_service = StrategyService(db_session)
        
        with pytest.raises(Exception):  # Should raise AIError
            await strategy_service._call_groq_api({"test": "data"})
    
    @pytest.mark.asyncio
    @patch('httpx.AsyncClient.get')
    async def test_get_market_data(self, mock_get, db_session):
        """Test market data collection."""
        # Mock API responses
        mock_response = AsyncMock()
        mock_response.json.return_value = {"pools": []}
        mock_get.return_value = mock_response
        
        strategy_service = StrategyService(db_session)
        market_data = await strategy_service._get_market_data()
        
        assert "alex_pools" in market_data
        assert "arkadiko_pools" in market_data
        assert "velar_pools" in market_data
    
    @pytest.mark.asyncio
    async def test_collect_user_data(self, db_session, test_user, test_wallet: Wallet):
        """Test user data collection."""
        strategy_service = StrategyService(db_session)
        
        with patch.object(strategy_service.wallet_service, 'get_wallet_balances') as mock_balances:
            mock_balances.return_value = {"stx": {"balance": "1000000"}}
            
            user_data = await strategy_service._collect_user_data(test_user.id)
            
            assert "wallets" in user_data
            assert "total_wallets" in user_data
            assert user_data["total_wallets"] == 1
    
    @pytest.mark.asyncio
    async def test_execute_strategy(self, db_session, test_recommendation: Recommendation):
        """Test strategy execution."""
        strategy_service = StrategyService(db_session)
        
        result = await strategy_service.execute_strategy(
            recommendation=test_recommendation,
            transaction_signature="0xabcdef1234567890",
            gas_fee=25000
        )
        
        assert "transaction_hash" in result
        assert "status" in result
        assert result["status"] == "pending"
        
        # Verify recommendation status was updated
        updated_recommendation = await strategy_service.get_recommendation_by_id(test_recommendation.id)
        assert updated_recommendation.status == "executed"
        assert updated_recommendation.executed_at is not None
    
    def test_create_strategy_prompt(self, db_session):
        """Test strategy prompt creation."""
        strategy_service = StrategyService(db_session)
        input_data = {
            "user_profile": {
                "risk_tolerance": "medium",
                "investment_amount": 1000,
                "time_horizon": "long"
            },
            "wallet_data": {"wallets": []},
            "market_data": {"pools": []}
        }
        
        prompt = strategy_service._create_strategy_prompt(input_data)
        
        assert "medium" in prompt
        assert "1000" in prompt
        assert "long" in prompt
        assert "JSON response" in prompt
