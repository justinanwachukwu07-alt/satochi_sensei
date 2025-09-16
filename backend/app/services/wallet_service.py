"""
Wallet service for blockchain wallet management
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import List, Optional, Dict, Any
import uuid
import httpx
import asyncio
from datetime import datetime

from app.core.config import settings
from app.core.exceptions import ExternalAPIError, BlockchainError
from app.models.wallet import Wallet, NetworkType
from app.models.user import User


class WalletService:
    """Service for managing blockchain wallets"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_wallet_by_id(self, wallet_id: str) -> Optional[Wallet]:
        """Get wallet by ID"""
        result = await self.db.execute(
            select(Wallet).where(Wallet.id == wallet_id)
        )
        return result.scalar_one_or_none()
    
    async def get_wallet_by_address(self, address: str, network: NetworkType) -> Optional[Wallet]:
        """Get wallet by address and network"""
        result = await self.db.execute(
            select(Wallet).where(
                Wallet.address == address,
                Wallet.network == network
            )
        )
        return result.scalar_one_or_none()
    
    async def get_user_wallets(self, user_id: str) -> List[Wallet]:
        """Get all wallets for a user"""
        result = await self.db.execute(
            select(Wallet)
            .where(Wallet.user_id == user_id)
            .where(Wallet.is_active == True)
            .order_by(Wallet.created_at.desc())
        )
        return result.scalars().all()
    
    async def create_wallet(
        self, 
        user_id: str, 
        address: str, 
        network: NetworkType,
        label: Optional[str] = None
    ) -> Wallet:
        """Create a new wallet connection"""
        wallet = Wallet(
            user_id=user_id,
            address=address,
            network=network,
            label=label
        )
        
        self.db.add(wallet)
        await self.db.commit()
        await self.db.refresh(wallet)
        
        return wallet
    
    async def disconnect_wallet(self, wallet_id: str) -> None:
        """Disconnect a wallet (soft delete)"""
        wallet = await self.get_wallet_by_id(wallet_id)
        if wallet:
            wallet.is_active = False
            await self.db.commit()
    
    async def get_wallet_balances(self, wallet: Wallet) -> Dict[str, Any]:
        """Get wallet balances from blockchain"""
        if wallet.network == NetworkType.STACKS:
            return await self._get_stacks_balances(wallet.address)
        elif wallet.network == NetworkType.BITCOIN:
            return await self._get_bitcoin_balances(wallet.address)
        else:
            raise BlockchainError(f"Unsupported network: {wallet.network}")
    
    async def _get_stacks_balances(self, address: str) -> Dict[str, Any]:
        """Get Stacks wallet balances"""
        try:
            async with httpx.AsyncClient() as client:
                # Get STX balance
                stx_response = await client.get(
                    f"{settings.STACKS_API_URL}/extended/v1/address/{address}/stx"
                )
                stx_data = stx_response.json()
                
                # Get token balances
                tokens_response = await client.get(
                    f"{settings.STACKS_API_URL}/extended/v1/tokens/nft-holders"
                )
                tokens_data = tokens_response.json()
                
                return {
                    "stx": {
                        "balance": stx_data.get("balance", "0"),
                        "total_sent": stx_data.get("total_sent", "0"),
                        "total_received": stx_data.get("total_received", "0"),
                        "total_fees_sent": stx_data.get("total_fees_sent", "0")
                    },
                    "tokens": tokens_data.get("results", []),
                    "network": "stacks"
                }
        except Exception as e:
            raise ExternalAPIError(f"Failed to fetch Stacks balances: {str(e)}")
    
    async def _get_bitcoin_balances(self, address: str) -> Dict[str, Any]:
        """Get Bitcoin wallet balances"""
        try:
            async with httpx.AsyncClient() as client:
                # Get address info
                response = await client.get(
                    f"{settings.BITCOIN_API_URL}/address/{address}"
                )
                data = response.json()
                
                return {
                    "btc": {
                        "balance": data.get("chain_stats", {}).get("funded_txo_sum", 0) - 
                                 data.get("chain_stats", {}).get("spent_txo_sum", 0),
                        "total_received": data.get("chain_stats", {}).get("funded_txo_sum", 0),
                        "total_sent": data.get("chain_stats", {}).get("spent_txo_sum", 0),
                        "tx_count": data.get("chain_stats", {}).get("tx_count", 0)
                    },
                    "network": "bitcoin"
                }
        except Exception as e:
            raise ExternalAPIError(f"Failed to fetch Bitcoin balances: {str(e)}")
    
    async def get_transaction_history(self, wallet: Wallet, limit: int = 50) -> List[Dict[str, Any]]:
        """Get transaction history for a wallet"""
        if wallet.network == NetworkType.STACKS:
            return await self._get_stacks_transactions(wallet.address, limit)
        elif wallet.network == NetworkType.BITCOIN:
            return await self._get_bitcoin_transactions(wallet.address, limit)
        else:
            raise BlockchainError(f"Unsupported network: {wallet.network}")
    
    async def _get_stacks_transactions(self, address: str, limit: int) -> List[Dict[str, Any]]:
        """Get Stacks transaction history"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{settings.STACKS_API_URL}/extended/v1/address/{address}/transactions",
                    params={"limit": limit}
                )
                data = response.json()
                return data.get("results", [])
        except Exception as e:
            raise ExternalAPIError(f"Failed to fetch Stacks transactions: {str(e)}")
    
    async def _get_bitcoin_transactions(self, address: str, limit: int) -> List[Dict[str, Any]]:
        """Get Bitcoin transaction history"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{settings.BITCOIN_API_URL}/address/{address}/txs",
                    params={"limit": limit}
                )
                return response.json()
        except Exception as e:
            raise ExternalAPIError(f"Failed to fetch Bitcoin transactions: {str(e)}")
