"""
Strategy service for AI-powered DeFi recommendations
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from typing import List, Optional, Dict, Any
import uuid
import httpx
import json
from datetime import datetime

from app.core.config import settings
from app.core.exceptions import AIError, ExternalAPIError
from app.models.recommendation import Recommendation
from app.models.user import User
from app.services.wallet_service import WalletService


class StrategyService:
    """Service for generating and managing DeFi strategy recommendations"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.wallet_service = WalletService(db)
    
    async def generate_recommendation(
        self,
        user_id: str,
        risk_tolerance: str = "medium",
        investment_amount: Optional[float] = None,
        time_horizon: str = "medium",
        preferred_protocols: Optional[List[str]] = None
    ) -> Recommendation:
        """Generate AI-powered DeFi strategy recommendation"""
        
        # Collect user data
        user_data = await self._collect_user_data(user_id)
        
        # Get market data
        market_data = await self._get_market_data()
        
        # Prepare input for AI
        ai_input = {
            "user_profile": {
                "risk_tolerance": risk_tolerance,
                "investment_amount": investment_amount,
                "time_horizon": time_horizon,
                "preferred_protocols": preferred_protocols or []
            },
            "wallet_data": user_data,
            "market_data": market_data,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Call Groq AI API
        ai_output = await self._call_groq_api(ai_input)
        
        # Create recommendation record
        recommendation = Recommendation(
            user_id=user_id,
            raw_input=ai_input,
            ai_output=ai_output,
            strategy_type=ai_output.get("strategy_type", "unknown"),
            risk_score=ai_output.get("risk_score", 0.5),
            expected_apy=ai_output.get("expected_apy"),
            explanation=ai_output.get("explanation"),
            status="pending"
        )
        
        self.db.add(recommendation)
        await self.db.commit()
        await self.db.refresh(recommendation)
        
        return recommendation
    
    async def _collect_user_data(self, user_id: str) -> Dict[str, Any]:
        """Collect user's wallet and portfolio data"""
        # Get user wallets
        wallets = await self.wallet_service.get_user_wallets(user_id)
        
        wallet_data = []
        for wallet in wallets:
            try:
                balances = await self.wallet_service.get_wallet_balances(wallet)
                wallet_data.append({
                    "address": wallet.address,
                    "network": wallet.network.value,
                    "balances": balances
                })
            except Exception as e:
                # Log error but continue with other wallets
                print(f"Error fetching balances for wallet {wallet.address}: {e}")
        
        return {
            "wallets": wallet_data,
            "total_wallets": len(wallets)
        }
    
    async def _get_market_data(self) -> Dict[str, Any]:
        """Get current DeFi market data"""
        try:
            async with httpx.AsyncClient() as client:
                # Get data from multiple sources
                market_data = {}
                
                # ALEX data
                try:
                    alex_response = await client.get(f"{settings.ALEX_API_URL}/pools")
                    market_data["alex_pools"] = alex_response.json()
                except:
                    market_data["alex_pools"] = []
                
                # Arkadiko data
                try:
                    arkadiko_response = await client.get(f"{settings.ARKADIKO_API_URL}/pools")
                    market_data["arkadiko_pools"] = arkadiko_response.json()
                except:
                    market_data["arkadiko_pools"] = []
                
                # Velar data
                try:
                    velar_response = await client.get(f"{settings.VELAR_API_URL}/pools")
                    market_data["velar_pools"] = velar_response.json()
                except:
                    market_data["velar_pools"] = []
                
                return market_data
        except Exception as e:
            raise ExternalAPIError(f"Failed to fetch market data: {str(e)}")
    
    async def _call_groq_api(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Call Groq AI API for strategy recommendations"""
        try:
            # Prepare prompt for Groq
            prompt = self._create_strategy_prompt(input_data)
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"https://api.groq.com/openai/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {settings.GROQ_API_KEY}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": settings.GROQ_MODEL,
                        "messages": [
                            {
                                "role": "system",
                                "content": "You are Satoshi Sensei, an expert DeFi advisor for Bitcoin and Stacks ecosystems. Provide actionable, safe, and profitable DeFi strategies based on user data and market conditions."
                            },
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ],
                        "temperature": 0.7,
                        "max_tokens": 2000
                    }
                )
                
                if response.status_code != 200:
                    raise AIError(f"Groq API error: {response.status_code}")
                
                result = response.json()
                ai_response = result["choices"][0]["message"]["content"]
                
                # Parse AI response (assuming it returns JSON)
                try:
                    return json.loads(ai_response)
                except json.JSONDecodeError:
                    # If not JSON, create structured response
                    return {
                        "strategy_type": "general_advice",
                        "risk_score": 0.5,
                        "explanation": ai_response,
                        "recommendations": [],
                        "expected_apy": None
                    }
        except Exception as e:
            raise AIError(f"Failed to get AI recommendation: {str(e)}")
    
    def _create_strategy_prompt(self, input_data: Dict[str, Any]) -> str:
        """Create prompt for Groq AI"""
        # Safely extract user profile data with defaults
        user_profile = input_data.get('user_profile', {})
        risk_tolerance = user_profile.get('risk_tolerance', 'medium')
        investment_amount = user_profile.get('investment_amount', 'Not specified')
        time_horizon = user_profile.get('time_horizon', 'medium')
        preferred_protocols = user_profile.get('preferred_protocols', [])
        
        return f"""
        Analyze the following user data and market conditions to provide a DeFi strategy recommendation:
        
        User Profile:
        - Risk Tolerance: {risk_tolerance}
        - Investment Amount: {investment_amount}
        - Time Horizon: {time_horizon}
        - Preferred Protocols: {preferred_protocols}
        
        Wallet Data:
        {json.dumps(input_data.get('wallet_data', {}), indent=2)}
        
        Market Data:
        {json.dumps(input_data.get('market_data', {}), indent=2)}
        
        Please provide a JSON response with the following structure:
        {{
            "strategy_type": "liquidity_provision|yield_farming|staking|arbitrage|other",
            "risk_score": 0.0-1.0,
            "expected_apy": percentage or null,
            "explanation": "Clear explanation of the strategy",
            "recommendations": [
                {{
                    "protocol": "protocol_name",
                    "action": "specific_action",
                    "amount": "suggested_amount",
                    "reasoning": "why this is recommended"
                }}
            ],
            "warnings": ["any risks or warnings"],
            "next_steps": ["actionable steps for the user"]
        }}
        """
    
    async def get_user_recommendations(
        self, 
        user_id: str, 
        limit: int = 10
    ) -> List[Recommendation]:
        """Get user's recommendation history"""
        result = await self.db.execute(
            select(Recommendation)
            .where(Recommendation.user_id == user_id)
            .order_by(desc(Recommendation.created_at))
            .limit(limit)
        )
        return result.scalars().all()
    
    async def get_recommendation_by_id(self, recommendation_id: str) -> Optional[Recommendation]:
        """Get recommendation by ID"""
        result = await self.db.execute(
            select(Recommendation).where(Recommendation.id == recommendation_id)
        )
        return result.scalar_one_or_none()
    
    async def execute_strategy(
        self,
        recommendation: Recommendation,
        transaction_signature: str,
        gas_fee: Optional[float] = None
    ) -> Dict[str, Any]:
        """Execute a strategy recommendation"""
        try:
            # Update recommendation status
            recommendation.status = "executed"
            recommendation.executed_at = datetime.utcnow()
            await self.db.commit()
            
            # In a real implementation, this would:
            # 1. Validate the transaction signature
            # 2. Broadcast the transaction to the blockchain
            # 3. Monitor transaction status
            # 4. Update recommendation with transaction hash
            
            # For now, return a mock response
            return {
                "transaction_hash": "0x" + "0" * 64,  # Mock hash
                "status": "pending",
                "estimated_confirmation_time": "2-5 minutes",
                "gas_used": gas_fee
            }
        except Exception as e:
            recommendation.status = "failed"
            await self.db.commit()
            raise AIError(f"Failed to execute strategy: {str(e)}")
