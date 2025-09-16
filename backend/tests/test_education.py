"""
Education endpoints tests
"""

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from unittest.mock import patch, AsyncMock
import json

from app.services.education_service import EducationService


@pytest.mark.education
class TestEducationEndpoints:
    """Test education endpoints."""
    
    @patch('app.services.education_service.EducationService.get_education_content')
    def test_get_education_content_success(self, mock_get_content, client: TestClient, auth_headers: dict):
        """Test successful education content retrieval."""
        mock_get_content.return_value = {
            "topic": "liquidity_provision",
            "level": "beginner",
            "explanation": "Liquidity provision is the act of depositing tokens...",
            "key_concepts": ["DEX", "Trading Pairs", "Fees"],
            "examples": [{"title": "ALEX DEX Pool", "description": "Provide STX/USDA liquidity"}],
            "related_topics": ["Yield Farming", "AMM"],
            "resources": [{"title": "ALEX Documentation", "url": "https://docs.alexlab.co", "type": "documentation"}]
        }
        
        response = client.get(
            "/api/v1/education/liquidity_provision?level=beginner",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["topic"] == "liquidity_provision"
        assert data["level"] == "beginner"
        assert "explanation" in data
        assert "key_concepts" in data
        assert "examples" in data
        assert "related_topics" in data
        assert "resources" in data
    
    def test_get_education_content_unauthorized(self, client: TestClient):
        """Test education content without authentication."""
        response = client.get("/api/v1/education/liquidity_provision")
        assert response.status_code == 403
    
    @patch('app.services.education_service.EducationService.explain_concept')
    def test_explain_concept_success(self, mock_explain, client: TestClient, auth_headers: dict, sample_education_request: dict):
        """Test successful concept explanation."""
        mock_explain.return_value = {
            "topic": "liquidity_provision",
            "level": "beginner",
            "explanation": "Custom explanation for liquidity provision...",
            "key_concepts": ["DEX", "AMM"],
            "examples": [{"title": "Example", "description": "Detailed example"}],
            "related_topics": ["Yield Farming"],
            "resources": [{"title": "Resource", "url": "https://example.com", "type": "article"}]
        }
        
        response = client.post(
            "/api/v1/education/explain",
            json=sample_education_request,
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["topic"] == sample_education_request["topic"]
        assert data["level"] == sample_education_request["level"]
        assert "explanation" in data
    
    def test_explain_concept_unauthorized(self, client: TestClient, sample_education_request: dict):
        """Test concept explanation without authentication."""
        response = client.post(
            "/api/v1/education/explain",
            json=sample_education_request
        )
        assert response.status_code == 403
    
    @patch('app.services.education_service.EducationService.get_available_topics')
    def test_list_education_topics(self, mock_get_topics, client: TestClient, auth_headers: dict):
        """Test listing available education topics."""
        mock_get_topics.return_value = [
            "liquidity_provision",
            "yield_farming",
            "staking",
            "defi_protocols"
        ]
        
        response = client.get("/api/v1/education/topics/list", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert "topics" in data
        assert isinstance(data["topics"], list)
        assert len(data["topics"]) == 4
    
    def test_list_education_topics_unauthorized(self, client: TestClient):
        """Test listing topics without authentication."""
        response = client.get("/api/v1/education/topics/list")
        assert response.status_code == 403


@pytest.mark.education
class TestEducationService:
    """Test education service."""
    
    @pytest.mark.asyncio
    @patch('httpx.AsyncClient.post')
    async def test_call_groq_education_api_success(self, mock_post, db_session):
        """Test successful Groq education API call."""
        # Mock Groq API response
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{
                "message": {
                    "content": json.dumps({
                        "topic": "liquidity_provision",
                        "level": "beginner",
                        "explanation": "Liquidity provision explanation...",
                        "key_concepts": ["DEX", "AMM"],
                        "examples": [{"title": "Example", "description": "Description"}],
                        "related_topics": ["Yield Farming"],
                        "resources": [{"title": "Resource", "url": "https://example.com", "type": "article"}]
                    })
                }
            }]
        }
        mock_post.return_value = mock_response
        
        education_service = EducationService(db_session)
        result = await education_service._call_groq_education_api(
            "liquidity_provision",
            "beginner",
            "test context"
        )
        
        assert result["topic"] == "liquidity_provision"
        assert result["level"] == "beginner"
        assert "explanation" in result
        assert "key_concepts" in result
    
    @pytest.mark.asyncio
    @patch('httpx.AsyncClient.post')
    async def test_call_groq_education_api_invalid_json(self, mock_post, db_session):
        """Test Groq education API call with invalid JSON response."""
        # Mock Groq API response with non-JSON content
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{
                "message": {
                    "content": "This is not JSON content"
                }
            }]
        }
        mock_post.return_value = mock_response
        
        education_service = EducationService(db_session)
        result = await education_service._call_groq_education_api(
            "liquidity_provision",
            "beginner"
        )
        
        assert result["topic"] == "liquidity_provision"
        assert result["level"] == "beginner"
        assert result["explanation"] == "This is not JSON content"
        assert result["key_concepts"] == []
    
    @pytest.mark.asyncio
    @patch('httpx.AsyncClient.post')
    async def test_call_groq_education_api_error(self, mock_post, db_session):
        """Test Groq education API call with error response."""
        # Mock Groq API error response
        mock_response = AsyncMock()
        mock_response.status_code = 500
        mock_post.return_value = mock_response
        
        education_service = EducationService(db_session)
        
        with pytest.raises(Exception):  # Should raise AIError
            await education_service._call_groq_education_api(
                "liquidity_provision",
                "beginner"
            )
    
    @pytest.mark.asyncio
    @patch('app.services.education_service.EducationService._call_groq_education_api')
    async def test_get_education_content_success(self, mock_groq, db_session):
        """Test successful education content retrieval."""
        mock_groq.return_value = {
            "topic": "liquidity_provision",
            "level": "beginner",
            "explanation": "Test explanation",
            "key_concepts": ["DEX"],
            "examples": [],
            "related_topics": [],
            "resources": []
        }
        
        education_service = EducationService(db_session)
        result = await education_service.get_education_content(
            "liquidity_provision",
            "beginner",
            "test context"
        )
        
        assert result["topic"] == "liquidity_provision"
        assert result["level"] == "beginner"
        mock_groq.assert_called_once_with("liquidity_provision", "beginner", "test context")
    
    @pytest.mark.asyncio
    @patch('app.services.education_service.EducationService._call_groq_education_api')
    async def test_get_education_content_fallback(self, mock_groq, db_session):
        """Test education content with fallback to static content."""
        mock_groq.side_effect = Exception("API Error")
        
        education_service = EducationService(db_session)
        result = await education_service.get_education_content(
            "liquidity_provision",
            "beginner"
        )
        
        assert result["topic"] == "liquidity_provision"
        assert result["level"] == "beginner"
        assert "explanation" in result
    
    @pytest.mark.asyncio
    async def test_explain_concept(self, db_session):
        """Test concept explanation."""
        education_service = EducationService(db_session)
        
        with patch.object(education_service, 'get_education_content') as mock_get_content:
            mock_get_content.return_value = {
                "topic": "yield_farming",
                "level": "intermediate",
                "explanation": "Yield farming explanation",
                "key_concepts": [],
                "examples": [],
                "related_topics": [],
                "resources": []
            }
            
            result = await education_service.explain_concept(
                "yield_farming",
                "intermediate",
                "test context"
            )
            
            assert result["topic"] == "yield_farming"
            assert result["level"] == "intermediate"
            mock_get_content.assert_called_once_with("yield_farming", "intermediate", "test context")
    
    @pytest.mark.asyncio
    async def test_get_available_topics(self, db_session):
        """Test getting available topics."""
        education_service = EducationService(db_session)
        topics = await education_service.get_available_topics()
        
        assert isinstance(topics, list)
        assert len(topics) > 0
        assert "liquidity_provision" in topics
        assert "yield_farming" in topics
        assert "staking" in topics
    
    def test_get_static_education_content(self, db_session):
        """Test static education content fallback."""
        education_service = EducationService(db_session)
        
        # Test with known topic
        result = education_service._get_static_education_content("liquidity_provision", "beginner")
        assert result["topic"] == "liquidity_provision"
        assert result["level"] == "beginner"
        assert "explanation" in result
        assert "key_concepts" in result
        
        # Test with unknown topic
        result = education_service._get_static_education_content("unknown_topic", "beginner")
        assert result["topic"] == "unknown_topic"
        assert result["level"] == "beginner"
        assert "not available" in result["explanation"]
    
    def test_create_education_prompt(self, db_session):
        """Test education prompt creation."""
        education_service = EducationService(db_session)
        
        prompt = education_service._create_education_prompt(
            "liquidity_provision",
            "beginner",
            "test context"
        )
        
        assert "liquidity_provision" in prompt
        assert "beginner" in prompt
        assert "test context" in prompt
        assert "JSON response" in prompt
        assert "key_concepts" in prompt
        assert "examples" in prompt
