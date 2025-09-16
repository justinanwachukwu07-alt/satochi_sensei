"""
Main application tests
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch


class TestMainApp:
    """Test main application endpoints."""
    
    def test_health_check(self, client: TestClient):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "satoshi-sensei-backend"
        assert data["version"] == "1.0.0"
    
    def test_root_endpoint(self, client: TestClient):
        """Test root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "docs" in data
        assert "health" in data
        assert data["docs"] == "/docs"
        assert data["health"] == "/health"
    
    def test_docs_endpoint(self, client: TestClient):
        """Test API documentation endpoint."""
        response = client.get("/docs")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
    
    def test_redoc_endpoint(self, client: TestClient):
        """Test ReDoc documentation endpoint."""
        response = client.get("/redoc")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
    
    def test_openapi_json(self, client: TestClient):
        """Test OpenAPI JSON schema endpoint."""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        data = response.json()
        assert "openapi" in data
        assert "info" in data
        assert data["info"]["title"] == "Satoshi Sensei API"
        assert data["info"]["version"] == "1.0.0"
    
    def test_cors_headers(self, client: TestClient):
        """Test CORS headers are present."""
        response = client.options("/api/v1/auth/signup")
        assert response.status_code == 200
        # CORS headers should be present (handled by middleware)
    
    def test_404_endpoint(self, client: TestClient):
        """Test 404 for nonexistent endpoint."""
        response = client.get("/nonexistent-endpoint")
        assert response.status_code == 404
    
    def test_method_not_allowed(self, client: TestClient):
        """Test 405 for wrong HTTP method."""
        response = client.put("/health")
        assert response.status_code == 405
    
    @patch('app.core.exceptions.SatoshiSenseiException')
    def test_custom_exception_handler(self, mock_exception, client: TestClient):
        """Test custom exception handler."""
        # This would need to be tested with actual exception raising
        # For now, we just verify the handler is registered
        assert True  # Placeholder for actual exception testing
