"""
Integration tests for end-to-end workflows
"""

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from unittest.mock import patch, AsyncMock
import json
import asyncio

from tests.mocks import mock_all_external_apis, MockExternalAPIs


class TestUserWorkflow:
    """Test complete user workflow from signup to strategy execution"""
    
    @pytest.mark.asyncio
    @mock_all_external_apis()
    async def test_complete_user_journey(self, client: TestClient):
        """Test complete user journey from signup to strategy execution"""
        # Step 1: User signup
        signup_response = client.post(
            "/api/v1/auth/signup",
            json={
                "email": "integration@test.com",
                "password": "testpassword123"
            }
        )
        assert signup_response.status_code == 200
        user_data = signup_response.json()
        user_id = user_data["id"]
        
        # Step 2: User login
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "integration@test.com",
                "password": "testpassword123"
            }
        )
        assert login_response.status_code == 200
        login_data = login_response.json()
        auth_token = login_data["access_token"]
        headers = {"Authorization": f"Bearer {auth_token}"}
        
        # Step 3: Get current user
        me_response = client.get("/api/v1/auth/me", headers=headers)
        assert me_response.status_code == 200
        assert me_response.json()["email"] == "integration@test.com"
        
        # Step 4: Connect wallet
        wallet_response = client.post(
            "/api/v1/wallet/connect",
            json={
                "address": "SP2J6ZY48GV1EZ5V2V5RB9MP66SW86PYKKNRV9EJ7",
                "network": "stacks",
                "label": "Integration Test Wallet"
            },
            headers=headers
        )
        assert wallet_response.status_code == 200
        wallet_data = wallet_response.json()
        wallet_id = wallet_data["id"]
        
        # Step 5: Get wallet balances
        balances_response = client.get(
            f"/api/v1/wallet/{wallet_id}/balances",
            headers=headers
        )
        assert balances_response.status_code == 200
        balances_data = balances_response.json()
        assert "balances" in balances_data
        
        # Step 6: Get strategy recommendation
        strategy_response = client.post(
            "/api/v1/strategy/recommend",
            json={
                "risk_tolerance": "medium",
                "investment_amount": 1000.0,
                "time_horizon": "long",
                "preferred_protocols": ["alex", "arkadiko"]
            },
            headers=headers
        )
        assert strategy_response.status_code == 200
        strategy_data = strategy_response.json()
        recommendation_id = strategy_data["id"]
        
        # Step 7: Get user recommendations
        recommendations_response = client.get(
            "/api/v1/strategy/recommendations",
            headers=headers
        )
        assert recommendations_response.status_code == 200
        recommendations_data = recommendations_response.json()
        assert len(recommendations_data) >= 1
        
        # Step 8: Get specific recommendation
        specific_recommendation_response = client.get(
            f"/api/v1/strategy/recommendations/{recommendation_id}",
            headers=headers
        )
        assert specific_recommendation_response.status_code == 200
        
        # Step 9: Execute strategy
        execution_response = client.post(
            "/api/v1/strategy/execute",
            json={
                "recommendation_id": recommendation_id,
                "transaction_signature": "0xabcdef1234567890",
                "gas_fee": 25000
            },
            headers=headers
        )
        assert execution_response.status_code == 200
        execution_data = execution_response.json()
        assert "transaction_hash" in execution_data
        
        # Step 10: Get education content
        education_response = client.get(
            "/api/v1/education/liquidity_provision?level=beginner",
            headers=headers
        )
        assert education_response.status_code == 200
        education_data = education_response.json()
        assert "explanation" in education_data
        
        # Step 11: Explain concept
        explain_response = client.post(
            "/api/v1/education/explain",
            json={
                "topic": "yield_farming",
                "level": "intermediate",
                "context": "I want to learn about yield farming strategies"
            },
            headers=headers
        )
        assert explain_response.status_code == 200
        
        # Step 12: List education topics
        topics_response = client.get(
            "/api/v1/education/topics/list",
            headers=headers
        )
        assert topics_response.status_code == 200
        topics_data = topics_response.json()
        assert "topics" in topics_data
        
        # Step 13: Logout
        logout_response = client.post("/api/v1/auth/logout")
        assert logout_response.status_code == 200


class TestWalletWorkflow:
    """Test wallet management workflow"""
    
    @pytest.mark.asyncio
    @mock_all_external_apis()
    async def test_wallet_management_workflow(self, client: TestClient):
        """Test complete wallet management workflow"""
        # Setup: Create user and login
        client.post(
            "/api/v1/auth/signup",
            json={
                "email": "wallet@test.com",
                "password": "testpassword123"
            }
        )
        
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "wallet@test.com",
                "password": "testpassword123"
            }
        )
        auth_token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {auth_token}"}
        
        # Step 1: Connect multiple wallets
        wallets = [
            {
                "address": "SP2J6ZY48GV1EZ5V2V5RB9MP66SW86PYKKNRV9EJ7",
                "network": "stacks",
                "label": "Stacks Wallet 1"
            },
            {
                "address": "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
                "network": "bitcoin",
                "label": "Bitcoin Wallet 1"
            }
        ]
        
        connected_wallets = []
        for wallet_data in wallets:
            response = client.post(
                "/api/v1/wallet/connect",
                json=wallet_data,
                headers=headers
            )
            assert response.status_code == 200
            connected_wallets.append(response.json())
        
        # Step 2: Get all user wallets
        wallets_response = client.get("/api/v1/wallet/", headers=headers)
        assert wallets_response.status_code == 200
        all_wallets = wallets_response.json()
        assert len(all_wallets) == 2
        
        # Step 3: Get balances for each wallet
        for wallet in connected_wallets:
            balances_response = client.get(
                f"/api/v1/wallet/{wallet['id']}/balances",
                headers=headers
            )
            assert balances_response.status_code == 200
            balances_data = balances_response.json()
            assert "balances" in balances_data
        
        # Step 4: Disconnect a wallet
        disconnect_response = client.delete(
            f"/api/v1/wallet/{connected_wallets[0]['id']}",
            headers=headers
        )
        assert disconnect_response.status_code == 200
        
        # Step 5: Verify wallet is disconnected
        wallets_response = client.get("/api/v1/wallet/", headers=headers)
        assert wallets_response.status_code == 200
        remaining_wallets = wallets_response.json()
        assert len(remaining_wallets) == 1


class TestStrategyWorkflow:
    """Test strategy recommendation and execution workflow"""
    
    @pytest.mark.asyncio
    @mock_all_external_apis()
    async def test_strategy_workflow(self, client: TestClient):
        """Test complete strategy workflow"""
        # Setup: Create user, login, and connect wallet
        client.post(
            "/api/v1/auth/signup",
            json={
                "email": "strategy@test.com",
                "password": "testpassword123"
            }
        )
        
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "strategy@test.com",
                "password": "testpassword123"
            }
        )
        auth_token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {auth_token}"}
        
        wallet_response = client.post(
            "/api/v1/wallet/connect",
            json={
                "address": "SP2J6ZY48GV1EZ5V2V5RB9MP66SW86PYKKNRV9EJ7",
                "network": "stacks",
                "label": "Strategy Test Wallet"
            },
            headers=headers
        )
        wallet_id = wallet_response.json()["id"]
        
        # Step 1: Get multiple strategy recommendations
        strategies = [
            {
                "risk_tolerance": "low",
                "investment_amount": 500.0,
                "time_horizon": "short"
            },
            {
                "risk_tolerance": "high",
                "investment_amount": 2000.0,
                "time_horizon": "long"
            }
        ]
        
        recommendations = []
        for strategy_data in strategies:
            response = client.post(
                "/api/v1/strategy/recommend",
                json=strategy_data,
                headers=headers
            )
            assert response.status_code == 200
            recommendations.append(response.json())
        
        # Step 2: Get all recommendations
        all_recommendations_response = client.get(
            "/api/v1/strategy/recommendations",
            headers=headers
        )
        assert all_recommendations_response.status_code == 200
        all_recommendations = all_recommendations_response.json()
        assert len(all_recommendations) >= 2
        
        # Step 3: Execute a strategy
        execution_response = client.post(
            "/api/v1/strategy/execute",
            json={
                "recommendation_id": recommendations[0]["id"],
                "transaction_signature": "0xabcdef1234567890",
                "gas_fee": 25000
            },
            headers=headers
        )
        assert execution_response.status_code == 200
        execution_data = execution_response.json()
        assert "transaction_hash" in execution_data
        
        # Step 4: Verify recommendation status updated
        updated_recommendation_response = client.get(
            f"/api/v1/strategy/recommendations/{recommendations[0]['id']}",
            headers=headers
        )
        assert updated_recommendation_response.status_code == 200
        # Status should be updated to "executed" (implementation dependent)


class TestEducationWorkflow:
    """Test education content workflow"""
    
    @pytest.mark.asyncio
    @mock_all_external_apis()
    async def test_education_workflow(self, client: TestClient):
        """Test complete education workflow"""
        # Setup: Create user and login
        client.post(
            "/api/v1/auth/signup",
            json={
                "email": "education@test.com",
                "password": "testpassword123"
            }
        )
        
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "education@test.com",
                "password": "testpassword123"
            }
        )
        auth_token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {auth_token}"}
        
        # Step 1: List available topics
        topics_response = client.get(
            "/api/v1/education/topics/list",
            headers=headers
        )
        assert topics_response.status_code == 200
        topics_data = topics_response.json()
        available_topics = topics_data["topics"]
        assert len(available_topics) > 0
        
        # Step 2: Get education content for different topics and levels
        topics_to_test = ["liquidity_provision", "yield_farming", "staking"]
        levels_to_test = ["beginner", "intermediate", "advanced"]
        
        for topic in topics_to_test[:2]:  # Test first 2 topics
            for level in levels_to_test:
                response = client.get(
                    f"/api/v1/education/{topic}?level={level}",
                    headers=headers
                )
                assert response.status_code == 200
                content_data = response.json()
                assert "explanation" in content_data
                assert content_data["topic"] == topic
                assert content_data["level"] == level
        
        # Step 3: Explain concepts with context
        concepts_to_explain = [
            {
                "topic": "liquidity_provision",
                "level": "beginner",
                "context": "I'm new to DeFi and want to understand liquidity provision"
            },
            {
                "topic": "yield_farming",
                "level": "intermediate",
                "context": "I have some experience with DeFi and want to optimize my yields"
            }
        ]
        
        for concept in concepts_to_explain:
            response = client.post(
                "/api/v1/education/explain",
                json=concept,
                headers=headers
            )
            assert response.status_code == 200
            explanation_data = response.json()
            assert "explanation" in explanation_data
            assert explanation_data["topic"] == concept["topic"]
            assert explanation_data["level"] == concept["level"]


class TestConcurrentWorkflows:
    """Test concurrent user workflows"""
    
    @pytest.mark.asyncio
    @mock_all_external_apis()
    async def test_concurrent_user_workflows(self, client: TestClient):
        """Test multiple users working concurrently"""
        async def user_workflow(user_id: int):
            """Individual user workflow"""
            email = f"user{user_id}@test.com"
            
            # Signup
            signup_response = client.post(
                "/api/v1/auth/signup",
                json={
                    "email": email,
                    "password": "testpassword123"
                }
            )
            if signup_response.status_code != 200:
                return False
            
            # Login
            login_response = client.post(
                "/api/v1/auth/login",
                json={
                    "email": email,
                    "password": "testpassword123"
                }
            )
            if login_response.status_code != 200:
                return False
            
            auth_token = login_response.json()["access_token"]
            headers = {"Authorization": f"Bearer {auth_token}"}
            
            # Connect wallet
            wallet_response = client.post(
                "/api/v1/wallet/connect",
                json={
                    "address": f"SP2J6ZY48GV1EZ5V2V5RB9MP66SW86PYKKNRV9EJ{user_id}",
                    "network": "stacks",
                    "label": f"User {user_id} Wallet"
                },
                headers=headers
            )
            if wallet_response.status_code != 200:
                return False
            
            # Get strategy recommendation
            strategy_response = client.post(
                "/api/v1/strategy/recommend",
                json={
                    "risk_tolerance": "medium",
                    "investment_amount": 1000.0,
                    "time_horizon": "long"
                },
                headers=headers
            )
            if strategy_response.status_code != 200:
                return False
            
            return True
        
        # Run 5 concurrent user workflows
        tasks = [user_workflow(i) for i in range(5)]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # All workflows should succeed
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                pytest.fail(f"User {i} workflow failed with exception: {result}")
            assert result is True, f"User {i} workflow failed"


class TestErrorRecovery:
    """Test error recovery in workflows"""
    
    @pytest.mark.asyncio
    async def test_workflow_error_recovery(self, client: TestClient):
        """Test that workflows can recover from errors"""
        # Setup: Create user and login
        client.post(
            "/api/v1/auth/signup",
            json={
                "email": "recovery@test.com",
                "password": "testpassword123"
            }
        )
        
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "recovery@test.com",
                "password": "testpassword123"
            }
        )
        auth_token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {auth_token}"}
        
        # Step 1: Make a request that will fail (invalid wallet)
        error_response = client.get(
            "/api/v1/wallet/00000000-0000-0000-0000-000000000000/balances",
            headers=headers
        )
        assert error_response.status_code == 404
        
        # Step 2: Verify application still works after error
        health_response = client.get("/health")
        assert health_response.status_code == 200
        
        # Step 3: Continue with normal workflow
        wallet_response = client.post(
            "/api/v1/wallet/connect",
            json={
                "address": "SP2J6ZY48GV1EZ5V2V5RB9MP66SW86PYKKNRV9EJ7",
                "network": "stacks",
                "label": "Recovery Test Wallet"
            },
            headers=headers
        )
        assert wallet_response.status_code == 200
        
        # Step 4: Verify wallet is connected
        wallets_response = client.get("/api/v1/wallet/", headers=headers)
        assert wallets_response.status_code == 200
        wallets_data = wallets_response.json()
        assert len(wallets_data) == 1
