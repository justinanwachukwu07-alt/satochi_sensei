"""
Wallet management endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uuid

from app.core.database import get_db
from app.core.exceptions import AuthenticationError, NotFoundError
from app.models.user import User
from app.models.wallet import Wallet, NetworkType
from app.services.auth_service import AuthService
from app.services.wallet_service import WalletService

router = APIRouter()
security = HTTPBearer()


class WalletConnectRequest(BaseModel):
    """Wallet connection request model"""
    address: str
    network: NetworkType
    label: Optional[str] = None


class WalletResponse(BaseModel):
    """Wallet response model"""
    id: str
    address: str
    network: NetworkType
    label: Optional[str]
    is_active: bool
    created_at: str


class WalletBalanceResponse(BaseModel):
    """Wallet balance response model"""
    address: str
    network: NetworkType
    balances: dict
    last_updated: str


@router.post("/connect", response_model=WalletResponse)
async def connect_wallet(
    wallet_data: WalletConnectRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    """Connect a new wallet to user account"""
    auth_service = AuthService(db)
    wallet_service = WalletService(db)
    
    # Get current user
    user = await auth_service.get_current_user(credentials.credentials)
    
    # Check if wallet already exists
    existing_wallet = await wallet_service.get_wallet_by_address(
        wallet_data.address, 
        wallet_data.network
    )
    
    if existing_wallet and existing_wallet.user_id == user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Wallet already connected"
        )
    
    # Create new wallet connection
    wallet = await wallet_service.create_wallet(
        user_id=user.id,
        address=wallet_data.address,
        network=wallet_data.network,
        label=wallet_data.label
    )
    
    return WalletResponse(
        id=str(wallet.id),
        address=wallet.address,
        network=wallet.network,
        label=wallet.label,
        is_active=wallet.is_active,
        created_at=wallet.created_at.isoformat()
    )


@router.get("/", response_model=List[WalletResponse])
async def get_user_wallets(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    """Get all wallets for the current user"""
    auth_service = AuthService(db)
    wallet_service = WalletService(db)
    
    # Get current user
    user = await auth_service.get_current_user(credentials.credentials)
    
    # Get user wallets
    wallets = await wallet_service.get_user_wallets(user.id)
    
    return [
        WalletResponse(
            id=str(wallet.id),
            address=wallet.address,
            network=wallet.network,
            label=wallet.label,
            is_active=wallet.is_active,
            created_at=wallet.created_at.isoformat()
        )
        for wallet in wallets
    ]


@router.get("/{wallet_id}/balances", response_model=WalletBalanceResponse)
async def get_wallet_balances(
    wallet_id: str,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    """Get balances for a specific wallet"""
    auth_service = AuthService(db)
    wallet_service = WalletService(db)
    
    # Get current user
    user = await auth_service.get_current_user(credentials.credentials)
    
    # Get wallet
    wallet = await wallet_service.get_wallet_by_id(uuid.UUID(wallet_id))
    
    if not wallet:
        raise NotFoundError("Wallet not found")
    
    if wallet.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    # Get wallet balances
    balances = await wallet_service.get_wallet_balances(wallet)
    
    return WalletBalanceResponse(
        address=wallet.address,
        network=wallet.network,
        balances=balances,
        last_updated=datetime.utcnow().isoformat()
    )


@router.delete("/{wallet_id}")
async def disconnect_wallet(
    wallet_id: str,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
):
    """Disconnect a wallet from user account"""
    auth_service = AuthService(db)
    wallet_service = WalletService(db)
    
    # Get current user
    user = await auth_service.get_current_user(credentials.credentials)
    
    # Get wallet
    wallet = await wallet_service.get_wallet_by_id(uuid.UUID(wallet_id))
    
    if not wallet:
        raise NotFoundError("Wallet not found")
    
    if wallet.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    # Disconnect wallet
    await wallet_service.disconnect_wallet(wallet.id)
    
    return {"message": "Wallet disconnected successfully"}
