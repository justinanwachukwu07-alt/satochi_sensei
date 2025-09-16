"""
Education service for DeFi learning and explanations
"""

from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any, List
import httpx
import json

from app.core.config import settings
from app.core.exceptions import AIError


class EducationService:
    """Service for providing educational content about DeFi"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_education_content(
        self,
        topic: str,
        level: str = "beginner",
        context: str = None
    ) -> Dict[str, Any]:
        """Get educational content about a DeFi topic"""
        try:
            # Call Groq AI for educational content
            content = await self._call_groq_education_api(topic, level, context)
            return content
        except Exception as e:
            # Fallback to static content
            return self._get_static_education_content(topic, level)
    
    async def explain_concept(
        self,
        topic: str,
        level: str = "beginner",
        context: str = None
    ) -> Dict[str, Any]:
        """Get AI-powered explanation of a DeFi concept"""
        return await self.get_education_content(topic, level, context)
    
    async def _call_groq_education_api(
        self,
        topic: str,
        level: str,
        context: str = None
    ) -> Dict[str, Any]:
        """Call Groq AI API for educational content"""
        try:
            prompt = self._create_education_prompt(topic, level, context)
            
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
                                "content": "You are Satoshi Sensei, an expert DeFi educator specializing in Bitcoin and Stacks ecosystems. Provide clear, accurate, and engaging educational content."
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
                
                # Parse AI response
                try:
                    return json.loads(ai_response)
                except json.JSONDecodeError:
                    # If not JSON, create structured response
                    return {
                        "topic": topic,
                        "level": level,
                        "explanation": ai_response,
                        "key_concepts": [],
                        "examples": [],
                        "related_topics": [],
                        "resources": []
                    }
        except Exception as e:
            raise AIError(f"Failed to get educational content: {str(e)}")
    
    def _create_education_prompt(self, topic: str, level: str, context: str = None) -> str:
        """Create prompt for Groq AI education"""
        context_text = f"\nContext: {context}" if context else ""
        
        return f"""
        Create educational content about "{topic}" for a {level} level audience.{context_text}
        
        Please provide a JSON response with the following structure:
        {{
            "topic": "{topic}",
            "level": "{level}",
            "explanation": "Clear, comprehensive explanation of the topic",
            "key_concepts": ["concept1", "concept2", "concept3"],
            "examples": [
                {{
                    "title": "Example title",
                    "description": "Detailed example explanation"
                }}
            ],
            "related_topics": ["related_topic1", "related_topic2"],
            "resources": [
                {{
                    "title": "Resource title",
                    "url": "resource_url",
                    "type": "article|video|documentation"
                }}
            ]
        }}
        
        Focus on practical, actionable information relevant to Bitcoin and Stacks DeFi ecosystems.
        """
    
    def _get_static_education_content(self, topic: str, level: str) -> Dict[str, Any]:
        """Fallback static educational content"""
        static_content = {
            "liquidity_provision": {
                "beginner": {
                    "explanation": "Liquidity provision is the act of depositing tokens into a decentralized exchange (DEX) pool to enable trading. In return, you earn fees from trades that happen in your pool.",
                    "key_concepts": ["DEX", "Trading Pairs", "Fees", "Impermanent Loss"],
                    "examples": [
                        {
                            "title": "ALEX DEX Pool",
                            "description": "Provide STX/USDA liquidity on ALEX to earn trading fees"
                        }
                    ],
                    "related_topics": ["Yield Farming", "AMM", "Staking"],
                    "resources": [
                        {
                            "title": "ALEX Documentation",
                            "url": "https://docs.alexlab.co",
                            "type": "documentation"
                        }
                    ]
                }
            },
            "yield_farming": {
                "beginner": {
                    "explanation": "Yield farming involves lending or staking your crypto assets to earn rewards, typically in the form of additional tokens or fees.",
                    "key_concepts": ["APY", "Rewards", "Staking", "Lending"],
                    "examples": [
                        {
                            "title": "Arkadiko Vaults",
                            "description": "Lock STX in Arkadiko vaults to earn yield on your collateral"
                        }
                    ],
                    "related_topics": ["Liquidity Provision", "DeFi Protocols", "Risk Management"],
                    "resources": [
                        {
                            "title": "Arkadiko Finance",
                            "url": "https://arkadiko.finance",
                            "type": "documentation"
                        }
                    ]
                }
            }
        }
        
        topic_content = static_content.get(topic.lower(), {})
        level_content = topic_content.get(level, {
            "explanation": f"Educational content about {topic} for {level} level is not available.",
            "key_concepts": [],
            "examples": [],
            "related_topics": [],
            "resources": []
        })
        
        return {
            "topic": topic,
            "level": level,
            **level_content
        }
    
    async def get_available_topics(self) -> List[str]:
        """Get list of available education topics"""
        return [
            "liquidity_provision",
            "yield_farming",
            "staking",
            "defi_protocols",
            "bitcoin_defi",
            "stacks_ecosystem",
            "smart_contracts",
            "tokenomics",
            "risk_management",
            "portfolio_diversification",
            "arbitrage",
            "lending_borrowing",
            "derivatives",
            "nft_defi",
            "cross_chain"
        ]
