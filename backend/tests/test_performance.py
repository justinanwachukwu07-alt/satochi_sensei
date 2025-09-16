"""
Performance and load testing
"""

import pytest
import asyncio
import time
import statistics
from fastapi.testclient import TestClient
from httpx import AsyncClient
from unittest.mock import patch, AsyncMock
import concurrent.futures
import threading

from tests.mocks import mock_all_external_apis


class TestPerformance:
    """Test application performance under various loads"""
    
    @pytest.mark.asyncio
    async def test_response_time_health_endpoint(self, client: TestClient):
        """Test response time for health endpoint"""
        response_times = []
        
        # Test 10 requests
        for _ in range(10):
            start_time = time.time()
            response = client.get("/health")
            end_time = time.time()
            
            assert response.status_code == 200
            response_times.append(end_time - start_time)
        
        # Calculate statistics
        avg_response_time = statistics.mean(response_times)
        max_response_time = max(response_times)
        min_response_time = min(response_times)
        
        # Assert performance requirements
        assert avg_response_time < 0.1, f"Average response time {avg_response_time:.3f}s exceeds 100ms"
        assert max_response_time < 0.5, f"Max response time {max_response_time:.3f}s exceeds 500ms"
        
        print(f"Health endpoint performance:")
        print(f"  Average: {avg_response_time:.3f}s")
        print(f"  Min: {min_response_time:.3f}s")
        print(f"  Max: {max_response_time:.3f}s")
    
    @pytest.mark.asyncio
    async def test_response_time_auth_endpoints(self, client: TestClient):
        """Test response time for authentication endpoints"""
        # Test signup performance
        signup_times = []
        for i in range(5):
            start_time = time.time()
            response = client.post(
                "/api/v1/auth/signup",
                json={
                    "email": f"perf{i}@test.com",
                    "password": "testpassword123"
                }
            )
            end_time = time.time()
            
            assert response.status_code == 200
            signup_times.append(end_time - start_time)
        
        # Test login performance
        login_times = []
        for i in range(5):
            start_time = time.time()
            response = client.post(
                "/api/v1/auth/login",
                json={
                    "email": f"perf{i}@test.com",
                    "password": "testpassword123"
                }
            )
            end_time = time.time()
            
            assert response.status_code == 200
            login_times.append(end_time - start_time)
        
        # Assert performance requirements
        avg_signup_time = statistics.mean(signup_times)
        avg_login_time = statistics.mean(login_times)
        
        assert avg_signup_time < 0.5, f"Average signup time {avg_signup_time:.3f}s exceeds 500ms"
        assert avg_login_time < 0.3, f"Average login time {avg_login_time:.3f}s exceeds 300ms"
        
        print(f"Auth endpoints performance:")
        print(f"  Signup average: {avg_signup_time:.3f}s")
        print(f"  Login average: {avg_login_time:.3f}s")
    
    @pytest.mark.asyncio
    @mock_all_external_apis()
    async def test_concurrent_requests(self, client: TestClient):
        """Test application under concurrent load"""
        # Setup: Create a user
        client.post(
            "/api/v1/auth/signup",
            json={
                "email": "concurrent@test.com",
                "password": "testpassword123"
            }
        )
        
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "concurrent@test.com",
                "password": "testpassword123"
            }
        )
        auth_token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {auth_token}"}
        
        # Test concurrent requests
        def make_request():
            response = client.get("/health")
            return response.status_code == 200
        
        # Run 20 concurrent requests
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            futures = [executor.submit(make_request) for _ in range(20)]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
        
        # All requests should succeed
        assert all(results), "Some concurrent requests failed"
        assert len(results) == 20, "Not all requests completed"
        
        print(f"Concurrent requests: {len(results)} successful")
    
    @pytest.mark.asyncio
    @mock_all_external_apis()
    async def test_memory_usage(self, client: TestClient):
        """Test memory usage under load"""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Create multiple users and perform operations
        for i in range(10):
            # Signup
            client.post(
                "/api/v1/auth/signup",
                json={
                    "email": f"memory{i}@test.com",
                    "password": "testpassword123"
                }
            )
            
            # Login
            login_response = client.post(
                "/api/v1/auth/login",
                json={
                    "email": f"memory{i}@test.com",
                    "password": "testpassword123"
                }
            )
            auth_token = login_response.json()["access_token"]
            headers = {"Authorization": f"Bearer {auth_token}"}
            
            # Connect wallet
            client.post(
                "/api/v1/wallet/connect",
                json={
                    "address": f"SP2J6ZY48GV1EZ5V2V5RB9MP66SW86PYKKNRV9EJ{i}",
                    "network": "stacks",
                    "label": f"Memory Test Wallet {i}"
                },
                headers=headers
            )
        
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        # Memory increase should be reasonable (less than 100MB for 10 users)
        assert memory_increase < 100, f"Memory increase {memory_increase:.1f}MB exceeds 100MB"
        
        print(f"Memory usage:")
        print(f"  Initial: {initial_memory:.1f}MB")
        print(f"  Final: {final_memory:.1f}MB")
        print(f"  Increase: {memory_increase:.1f}MB")
    
    @pytest.mark.asyncio
    async def test_database_performance(self, client: TestClient):
        """Test database performance under load"""
        # Create multiple users rapidly
        start_time = time.time()
        
        for i in range(20):
            response = client.post(
                "/api/v1/auth/signup",
                json={
                    "email": f"dbperf{i}@test.com",
                    "password": "testpassword123"
                }
            )
            assert response.status_code == 200
        
        end_time = time.time()
        total_time = end_time - start_time
        avg_time_per_user = total_time / 20
        
        # Should be able to create 20 users in less than 5 seconds
        assert total_time < 5.0, f"Creating 20 users took {total_time:.2f}s, exceeds 5s"
        assert avg_time_per_user < 0.5, f"Average time per user {avg_time_per_user:.3f}s exceeds 500ms"
        
        print(f"Database performance:")
        print(f"  20 users created in {total_time:.2f}s")
        print(f"  Average per user: {avg_time_per_user:.3f}s")
    
    @pytest.mark.asyncio
    @mock_all_external_apis()
    async def test_api_rate_limiting(self, client: TestClient):
        """Test API rate limiting behavior"""
        # Make rapid requests to test rate limiting
        response_times = []
        rate_limited = False
        
        for i in range(50):
            start_time = time.time()
            response = client.get("/health")
            end_time = time.time()
            
            response_times.append(end_time - start_time)
            
            if response.status_code == 429:
                rate_limited = True
                break
        
        # If rate limiting is implemented, it should kick in
        # If not implemented, all requests should succeed quickly
        if rate_limited:
            print("Rate limiting is working")
        else:
            # All requests should be fast
            avg_response_time = statistics.mean(response_times)
            assert avg_response_time < 0.1, f"Average response time {avg_response_time:.3f}s exceeds 100ms"
            print(f"No rate limiting detected, average response time: {avg_response_time:.3f}s")
    
    @pytest.mark.asyncio
    async def test_large_payload_handling(self, client: TestClient):
        """Test handling of large payloads"""
        # Test with large JSON payload
        large_payload = {
            "data": "x" * 10000,  # 10KB string
            "array": list(range(1000)),  # 1000 integers
            "nested": {
                "level1": {
                    "level2": {
                        "level3": "deep_value"
                    }
                }
            }
        }
        
        start_time = time.time()
        response = client.post(
            "/api/v1/strategy/recommend",
            json=large_payload,
            headers={"Authorization": "Bearer valid_token"}
        )
        end_time = time.time()
        
        # Should handle large payloads gracefully
        # Either process successfully or return appropriate error
        assert response.status_code in [200, 413, 403], f"Unexpected status code: {response.status_code}"
        
        response_time = end_time - start_time
        assert response_time < 2.0, f"Large payload handling took {response_time:.2f}s, exceeds 2s"
        
        print(f"Large payload handling: {response_time:.3f}s")
    
    @pytest.mark.asyncio
    async def test_error_handling_performance(self, client: TestClient):
        """Test performance of error handling"""
        error_endpoints = [
            "/api/v1/nonexistent",
            "/api/v1/auth/me",  # No auth
            "/api/v1/wallet/connect",  # No auth
        ]
        
        error_response_times = []
        
        for endpoint in error_endpoints:
            start_time = time.time()
            response = client.get(endpoint)
            end_time = time.time()
            
            # Should return error quickly
            assert response.status_code in [404, 403, 422]
            error_response_times.append(end_time - start_time)
        
        avg_error_time = statistics.mean(error_response_times)
        assert avg_error_time < 0.1, f"Average error response time {avg_error_time:.3f}s exceeds 100ms"
        
        print(f"Error handling performance: {avg_error_time:.3f}s average")
    
    @pytest.mark.asyncio
    @mock_all_external_apis()
    async def test_external_api_performance(self, client: TestClient):
        """Test performance with external API calls"""
        # Setup: Create user and login
        client.post(
            "/api/v1/auth/signup",
            json={
                "email": "external@test.com",
                "password": "testpassword123"
            }
        )
        
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "external@test.com",
                "password": "testpassword123"
            }
        )
        auth_token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {auth_token}"}
        
        # Connect wallet (triggers external API calls)
        start_time = time.time()
        wallet_response = client.post(
            "/api/v1/wallet/connect",
            json={
                "address": "SP2J6ZY48GV1EZ5V2V5RB9MP66SW86PYKKNRV9EJ7",
                "network": "stacks",
                "label": "External API Test Wallet"
            },
            headers=headers
        )
        end_time = time.time()
        
        assert wallet_response.status_code == 200
        wallet_time = end_time - start_time
        
        # Get balances (triggers external API calls)
        wallet_id = wallet_response.json()["id"]
        start_time = time.time()
        balances_response = client.get(
            f"/api/v1/wallet/{wallet_id}/balances",
            headers=headers
        )
        end_time = time.time()
        
        assert balances_response.status_code == 200
        balances_time = end_time - start_time
        
        # External API calls should be reasonably fast (with mocks)
        assert wallet_time < 1.0, f"Wallet connection took {wallet_time:.2f}s, exceeds 1s"
        assert balances_time < 1.0, f"Balance retrieval took {balances_time:.2f}s, exceeds 1s"
        
        print(f"External API performance:")
        print(f"  Wallet connection: {wallet_time:.3f}s")
        print(f"  Balance retrieval: {balances_time:.3f}s")
    
    @pytest.mark.asyncio
    async def test_concurrent_user_creation(self, client: TestClient):
        """Test concurrent user creation performance"""
        def create_user(user_id):
            response = client.post(
                "/api/v1/auth/signup",
                json={
                    "email": f"concurrent{user_id}@test.com",
                    "password": "testpassword123"
                }
            )
            return response.status_code == 200
        
        # Create 10 users concurrently
        start_time = time.time()
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(create_user, i) for i in range(10)]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # All users should be created successfully
        assert all(results), "Some concurrent user creations failed"
        assert total_time < 3.0, f"Concurrent user creation took {total_time:.2f}s, exceeds 3s"
        
        print(f"Concurrent user creation: {total_time:.2f}s for 10 users")
    
    @pytest.mark.asyncio
    async def test_memory_leak_detection(self, client: TestClient):
        """Test for memory leaks during repeated operations"""
        import psutil
        import os
        import gc
        
        process = psutil.Process(os.getpid())
        
        # Perform repeated operations
        for cycle in range(5):
            initial_memory = process.memory_info().rss / 1024 / 1024  # MB
            
            # Create and delete users
            for i in range(10):
                client.post(
                    "/api/v1/auth/signup",
                    json={
                        "email": f"leak{cycle}_{i}@test.com",
                        "password": "testpassword123"
                    }
                )
            
            # Force garbage collection
            gc.collect()
            
            final_memory = process.memory_info().rss / 1024 / 1024  # MB
            memory_increase = final_memory - initial_memory
            
            # Memory increase should be minimal
            assert memory_increase < 50, f"Memory leak detected: {memory_increase:.1f}MB increase in cycle {cycle}"
            
            print(f"Cycle {cycle}: Memory increase {memory_increase:.1f}MB")
        
        print("No significant memory leaks detected")
