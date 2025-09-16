"""
Mock utilities for external APIs and services
"""

import json
from unittest.mock import AsyncMock, MagicMock, patch
from typing import Dict, Any, List
import httpx


class MockGroqAPI:
    """Mock Groq API responses for testing"""
    
    @staticmethod
    def get_successful_strategy_response() -> Dict[str, Any]:
        """Mock successful strategy recommendation response"""
        return {
            "choices": [{
                "message": {
                    "content": json.dumps({
                        "strategy_type": "liquidity_provision",
                        "risk_score": 0.7,
                        "expected_apy": 12.5,
                        "explanation": "This is a test strategy for providing liquidity to ALEX DEX pools.",
                        "recommendations": [
                            {
                                "protocol": "alex",
                                "action": "add_liquidity",
                                "amount": "1000",
                                "reasoning": "High APY with moderate risk"
                            }
                        ],
                        "warnings": ["Impermanent loss risk"],
                        "next_steps": ["Connect wallet", "Approve tokens", "Add liquidity"]
                    })
                }
            }]
        }
    
    @staticmethod
    def get_education_response() -> Dict[str, Any]:
        """Mock education content response"""
        return {
            "choices": [{
                "message": {
                    "content": json.dumps({
                        "topic": "liquidity_provision",
                        "level": "beginner",
                        "explanation": "Liquidity provision is the act of depositing tokens into a decentralized exchange pool to earn trading fees.",
                        "key_concepts": ["DEX", "Trading Pairs", "Fees", "Impermanent Loss"],
                        "examples": [
                            {
                                "title": "ALEX DEX Pool",
                                "description": "Provide STX/USDA liquidity to earn fees"
                            }
                        ],
                        "related_topics": ["Yield Farming", "AMM"],
                        "resources": [
                            {
                                "title": "ALEX Documentation",
                                "url": "https://docs.alexlab.co",
                                "type": "documentation"
                            }
                        ]
                    })
                }
            }]
        }
    
    @staticmethod
    def get_invalid_json_response() -> Dict[str, Any]:
        """Mock response with invalid JSON"""
        return {
            "choices": [{
                "message": {
                    "content": "This is not valid JSON content"
                }
            }]
        }
    
    @staticmethod
    def get_error_response() -> Dict[str, Any]:
        """Mock error response"""
        return {
            "error": {
                "message": "API rate limit exceeded",
                "type": "rate_limit_error"
            }
        }


class MockStacksAPI:
    """Mock Stacks blockchain API responses"""
    
    @staticmethod
    def get_balance_response() -> Dict[str, Any]:
        """Mock Stacks balance response"""
        return {
            "balance": "1000000",
            "total_sent": "500000",
            "total_received": "1500000",
            "total_fees_sent": "10000",
            "lock_tx_id": None,
            "lock_height": None,
            "burnchain_lock_height": None,
            "burnchain_unlock_height": None
        }
    
    @staticmethod
    def get_token_balances_response() -> List[Dict[str, Any]]:
        """Mock token balances response"""
        return [
            {
                "token_asset_identifier": "SP2J6ZY48GV1EZ5V2V5RB9MP66SW86PYKKNRV9EJ7::alex-token::alex",
                "balance": "5000000"
            }
        ]
    
    @staticmethod
    def get_transaction_response() -> Dict[str, Any]:
        """Mock transaction response"""
        return {
            "tx_id": "0x1234567890abcdef",
            "tx_status": "success",
            "tx_result": "0x0100000000000000000000000000000001",
            "gas_used": 25000,
            "gas_price": "1000"
        }


class MockBitcoinAPI:
    """Mock Bitcoin blockchain API responses"""
    
    @staticmethod
    def get_address_info_response() -> Dict[str, Any]:
        """Mock Bitcoin address info response"""
        return {
            "address": "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
            "chain_stats": {
                "funded_txo_sum": 2000000,
                "funded_txo_count": 5,
                "spent_txo_sum": 1000000,
                "spent_txo_count": 3,
                "tx_count": 8
            },
            "mempool_stats": {
                "funded_txo_sum": 0,
                "funded_txo_count": 0,
                "spent_txo_sum": 0,
                "spent_txo_count": 0,
                "tx_count": 0
            }
        }
    
    @staticmethod
    def get_transaction_response() -> Dict[str, Any]:
        """Mock Bitcoin transaction response"""
        return {
            "txid": "0xabcdef1234567890",
            "status": {
                "confirmed": True,
                "block_height": 800000,
                "block_hash": "0xblockhash123",
                "block_time": 1640995200
            },
            "fee": 1000,
            "vsize": 250
        }


class MockExternalAPIs:
    """Centralized mock for all external APIs"""
    
    def __init__(self):
        self.groq = MockGroqAPI()
        self.stacks = MockStacksAPI()
        self.bitcoin = MockBitcoinAPI()
    
    def setup_groq_mocks(self):
        """Setup Groq API mocks"""
        return patch('httpx.AsyncClient.post', side_effect=self._mock_groq_post)
    
    def setup_stacks_mocks(self):
        """Setup Stacks API mocks"""
        return patch('httpx.AsyncClient.get', side_effect=self._mock_stacks_get)
    
    def setup_bitcoin_mocks(self):
        """Setup Bitcoin API mocks"""
        return patch('httpx.AsyncClient.get', side_effect=self._mock_bitcoin_get)
    
    def _mock_groq_post(self, *args, **kwargs):
        """Mock Groq POST requests"""
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.json.return_value = self.groq.get_successful_strategy_response()
        return mock_response
    
    def _mock_stacks_get(self, *args, **kwargs):
        """Mock Stacks GET requests"""
        mock_response = AsyncMock()
        mock_response.status_code = 200
        
        url = args[0] if args else kwargs.get('url', '')
        if 'balance' in url:
            mock_response.json.return_value = self.stacks.get_balance_response()
        elif 'token' in url:
            mock_response.json.return_value = self.stacks.get_token_balances_response()
        else:
            mock_response.json.return_value = self.stacks.get_transaction_response()
        
        return mock_response
    
    def _mock_bitcoin_get(self, *args, **kwargs):
        """Mock Bitcoin GET requests"""
        mock_response = AsyncMock()
        mock_response.status_code = 200
        
        url = args[0] if args else kwargs.get('url', '')
        if 'address' in url:
            mock_response.json.return_value = self.bitcoin.get_address_info_response()
        else:
            mock_response.json.return_value = self.bitcoin.get_transaction_response()
        
        return mock_response


# Global mock instance
mock_apis = MockExternalAPIs()


def mock_groq_success():
    """Decorator to mock successful Groq API calls"""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            with mock_apis.setup_groq_mocks():
                return await func(*args, **kwargs)
        return wrapper
    return decorator


def mock_groq_error():
    """Decorator to mock Groq API errors"""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            with patch('httpx.AsyncClient.post') as mock_post:
                mock_response = AsyncMock()
                mock_response.status_code = 500
                mock_post.return_value = mock_response
                return await func(*args, **kwargs)
        return wrapper
    return decorator


def mock_stacks_api():
    """Decorator to mock Stacks API calls"""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            with mock_apis.setup_stacks_mocks():
                return await func(*args, **kwargs)
        return wrapper
    return decorator


def mock_bitcoin_api():
    """Decorator to mock Bitcoin API calls"""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            with mock_apis.setup_bitcoin_mocks():
                return await func(*args, **kwargs)
        return wrapper
    return decorator


def mock_all_external_apis():
    """Decorator to mock all external APIs"""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            with mock_apis.setup_groq_mocks(), \
                 mock_apis.setup_stacks_mocks(), \
                 mock_apis.setup_bitcoin_mocks():
                return await func(*args, **kwargs)
        return wrapper
    return decorator
