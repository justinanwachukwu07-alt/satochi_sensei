"""
Main API router for v1 endpoints
"""

from fastapi import APIRouter

from app.api.v1.endpoints import auth, wallet, strategy, education

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(wallet.router, prefix="/wallet", tags=["wallet"])
api_router.include_router(strategy.router, prefix="/strategy", tags=["strategy"])
api_router.include_router(education.router, prefix="/education", tags=["education"])
