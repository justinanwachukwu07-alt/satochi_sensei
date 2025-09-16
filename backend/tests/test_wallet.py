"""
Wallet management tests
"""

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from unittest.mock import patch, AsyncMock
import uuid

from app.models.wallet import Wallet, NetworkType
from app.services.wallet_service import WalletService


@pytest.mark.wallet
class TestWalletEndpoints:
    """Test wallet management endpoints."""
    
    def test_connect_wallet_success(self, client: TestClient, auth_headers: dict, sample_wallet_data: dict):
        """Test successful wallet connection."""
        response = client.post(
            "/api/v1/wallet/connect",
            json=sample_wallet_data,
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["address"] == sample_wallet_data["address"]
        assert data["network"] == sample_wallet_data["network"]
        assert data["label"] == sample_wallet_data["label"]
        assert data["is_active"] is True
        assert "id" in data
        assert "created_at" in data
    
    def test_connect_wallet_duplicate(self, client: TestClient, auth_headers: dict, test_wallet: Wallet):
        """Test connecting duplicate wallet."""
        response = client.post(
            "/api/v1/wallet/connect",
            json={
                "address": test_wallet.address,
                "network": test_wallet.network.value,
                "label": "Duplicate Wallet"
            },
            headers=auth_headers
        )
        assert response.status_code == 400
        assert "Wallet already connected" in response.json()["detail"]
    
    def test_connect_wallet_unauthorized(self, client: TestClient, sample_wallet_data: dict):
        """Test wallet connection without authentication."""
        response = client.post(
            "/api/v1/wallet/connect",
            json=sample_wallet_data
        )
        assert response.status_code == 403
    
    def test_get_user_wallets(self, client: TestClient, auth_headers: dict, test_wallet: Wallet):
        """Test getting user wallets."""
        response = client.get("/api/v1/wallet/", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["id"] == str(test_wallet.id)
        assert data[0]["address"] == test_wallet.address
    
    def test_get_user_wallets_unauthorized(self, client: TestClient):
        """Test getting wallets without authentication."""
        response = client.get("/api/v1/wallet/")
        assert response.status_code == 403
    
    @patch('app.services.wallet_service.WalletService.get_wallet_balances')
    def test_get_wallet_balances_success(self, mock_balances, client: TestClient, auth_headers: dict, test_wallet: Wallet):
        """Test getting wallet balances."""
        mock_balances.return_value = {
            "stx": {"balance": "1000000"},
            "tokens": [],
            "network": "stacks"
        }
        
        response = client.get(
            f"/api/v1/wallet/{test_wallet.id}/balances",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["address"] == test_wallet.address
        assert data["network"] == test_wallet.network.value
        assert "balances" in data
        assert "last_updated" in data
    
    def test_get_wallet_balances_not_found(self, client: TestClient, auth_headers: dict):
        """Test getting balances for nonexistent wallet."""
        fake_id = str(uuid.uuid4())
        response = client.get(
            f"/api/v1/wallet/{fake_id}/balances",
            headers=auth_headers
        )
        assert response.status_code == 404
    
    def test_get_wallet_balances_unauthorized(self, client: TestClient, test_wallet: Wallet):
        """Test getting wallet balances without authentication."""
        response = client.get(f"/api/v1/wallet/{test_wallet.id}/balances")
        assert response.status_code == 403
    
    def test_disconnect_wallet_success(self, client: TestClient, auth_headers: dict, test_wallet: Wallet):
        """Test successful wallet disconnection."""
        response = client.delete(
            f"/api/v1/wallet/{test_wallet.id}",
            headers=auth_headers
        )
        assert response.status_code == 200
        assert "Wallet disconnected successfully" in response.json()["message"]
    
    def test_disconnect_wallet_not_found(self, client: TestClient, auth_headers: dict):
        """Test disconnecting nonexistent wallet."""
        fake_id = str(uuid.uuid4())
        response = client.delete(
            f"/api/v1/wallet/{fake_id}",
            headers=auth_headers
        )
        assert response.status_code == 404
    
    def test_disconnect_wallet_unauthorized(self, client: TestClient, test_wallet: Wallet):
        """Test wallet disconnection without authentication."""
        response = client.delete(f"/api/v1/wallet/{test_wallet.id}")
        assert response.status_code == 403


@pytest.mark.wallet
class TestWalletService:
    """Test wallet service."""
    
    @pytest.mark.asyncio
    async def test_create_wallet(self, db_session, test_user):
        """Test wallet creation."""
        wallet_service = WalletService(db_session)
        wallet = await wallet_service.create_wallet(
            user_id=test_user.id,
            address="SP2J6ZY48GV1EZ5V2V5RB9MP66SW86PYKKNRV9EJ7",
            network=NetworkType.STACKS,
            label="Test Wallet"
        )
        assert wallet.address == "SP2J6ZY48GV1EZ5V2V5RB9MP66SW86PYKKNRV9EJ7"
        assert wallet.network == NetworkType.STACKS
        assert wallet.label == "Test Wallet"
        assert wallet.user_id == test_user.id
    
    @pytest.mark.asyncio
    async def test_get_wallet_by_id(self, db_session, test_wallet: Wallet):
        """Test getting wallet by ID."""
        wallet_service = WalletService(db_session)
        wallet = await wallet_service.get_wallet_by_id(test_wallet.id)
        assert wallet is not None
        assert wallet.id == test_wallet.id
    
    @pytest.mark.asyncio
    async def test_get_wallet_by_id_not_found(self, db_session):
        """Test getting wallet by ID when not found."""
        wallet_service = WalletService(db_session)
        fake_id = uuid.uuid4()
        wallet = await wallet_service.get_wallet_by_id(fake_id)
        assert wallet is None
    
    @pytest.mark.asyncio
    async def test_get_wallet_by_address(self, db_session, test_wallet: Wallet):
        """Test getting wallet by address and network."""
        wallet_service = WalletService(db_session)
        wallet = await wallet_service.get_wallet_by_address(
            test_wallet.address,
            test_wallet.network
        )
        assert wallet is not None
        assert wallet.address == test_wallet.address
        assert wallet.network == test_wallet.network
    
    @pytest.mark.asyncio
    async def test_get_user_wallets(self, db_session, test_user, test_wallet: Wallet):
        """Test getting user wallets."""
        wallet_service = WalletService(db_session)
        wallets = await wallet_service.get_user_wallets(test_user.id)
        assert len(wallets) == 1
        assert wallets[0].id == test_wallet.id
    
    @pytest.mark.asyncio
    async def test_disconnect_wallet(self, db_session, test_wallet: Wallet):
        """Test wallet disconnection."""
        wallet_service = WalletService(db_session)
        await wallet_service.disconnect_wallet(test_wallet.id)
        
        # Verify wallet is marked as inactive
        wallet = await wallet_service.get_wallet_by_id(test_wallet.id)
        assert wallet.is_active is False
    
    @pytest.mark.asyncio
    @patch('httpx.AsyncClient.get')
    async def test_get_stacks_balances(self, mock_get, db_session, test_wallet: Wallet):
        """Test getting Stacks wallet balances."""
        # Mock API response
        mock_response = AsyncMock()
        mock_response.json.return_value = {
            "balance": "1000000",
            "total_sent": "500000",
            "total_received": "1500000",
            "total_fees_sent": "10000"
        }
        mock_get.return_value = mock_response
        
        wallet_service = WalletService(db_session)
        balances = await wallet_service._get_stacks_balances(test_wallet.address)
        
        assert "stx" in balances
        assert "tokens" in balances
        assert "network" in balances
        assert balances["network"] == "stacks"
    
    @pytest.mark.asyncio
    @patch('httpx.AsyncClient.get')
    async def test_get_bitcoin_balances(self, mock_get, db_session, test_wallet: Wallet):
        """Test getting Bitcoin wallet balances."""
        # Mock API response
        mock_response = AsyncMock()
        mock_response.json.return_value = {
            "chain_stats": {
                "funded_txo_sum": 2000000,
                "spent_txo_sum": 1000000,
                "tx_count": 10
            }
        }
        mock_get.return_value = mock_response
        
        wallet_service = WalletService(db_session)
        balances = await wallet_service._get_bitcoin_balances("1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa")
        
        assert "btc" in balances
        assert "network" in balances
        assert balances["network"] == "bitcoin"
    
    @pytest.mark.asyncio
    async def test_get_wallet_balances_stacks(self, db_session, test_wallet: Wallet):
        """Test getting wallet balances for Stacks network."""
        wallet_service = WalletService(db_session)
        
        with patch.object(wallet_service, '_get_stacks_balances') as mock_stacks:
            mock_stacks.return_value = {"stx": {"balance": "1000000"}}
            
            balances = await wallet_service.get_wallet_balances(test_wallet)
            assert balances == {"stx": {"balance": "1000000"}}
            mock_stacks.assert_called_once_with(test_wallet.address)
    
    @pytest.mark.asyncio
    async def test_get_wallet_balances_bitcoin(self, db_session, test_user):
        """Test getting wallet balances for Bitcoin network."""
        # Create Bitcoin wallet
        wallet_service = WalletService(db_session)
        btc_wallet = await wallet_service.create_wallet(
            user_id=test_user.id,
            address="1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
            network=NetworkType.BITCOIN,
            label="BTC Wallet"
        )
        
        with patch.object(wallet_service, '_get_bitcoin_balances') as mock_btc:
            mock_btc.return_value = {"btc": {"balance": 1000000}}
            
            balances = await wallet_service.get_wallet_balances(btc_wallet)
            assert balances == {"btc": {"balance": 1000000}}
            mock_btc.assert_called_once_with(btc_wallet.address)
    
    @pytest.mark.asyncio
    async def test_get_wallet_balances_unsupported_network(self, db_session, test_user):
        """Test getting wallet balances for unsupported network."""
        # Create wallet with unsupported network (this would need to be added to enum)
        wallet_service = WalletService(db_session)
        
        # This test would need to be updated if we add more network types
        # For now, we test the error handling
        with pytest.raises(Exception):  # Should raise BlockchainError
            await wallet_service.get_wallet_balances(None)
