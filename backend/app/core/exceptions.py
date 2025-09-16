"""
Custom exceptions for the application
"""

from fastapi import HTTPException, status


class SatoshiSenseiException(Exception):
    """Base exception for Satoshi Sensei"""
    
    def __init__(self, detail: str, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR):
        self.detail = detail
        self.status_code = status_code
        super().__init__(detail)


class AuthenticationError(SatoshiSenseiException):
    """Authentication related errors"""
    
    def __init__(self, detail: str = "Authentication failed"):
        super().__init__(detail, status.HTTP_401_UNAUTHORIZED)


class AuthorizationError(SatoshiSenseiException):
    """Authorization related errors"""
    
    def __init__(self, detail: str = "Insufficient permissions"):
        super().__init__(detail, status.HTTP_403_FORBIDDEN)


class ValidationError(SatoshiSenseiException):
    """Validation related errors"""
    
    def __init__(self, detail: str = "Validation failed"):
        super().__init__(detail, status.HTTP_422_UNPROCESSABLE_ENTITY)


class NotFoundError(SatoshiSenseiException):
    """Resource not found errors"""
    
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(detail, status.HTTP_404_NOT_FOUND)


class ExternalAPIError(SatoshiSenseiException):
    """External API related errors"""
    
    def __init__(self, detail: str = "External API error"):
        super().__init__(detail, status.HTTP_502_BAD_GATEWAY)


class BlockchainError(SatoshiSenseiException):
    """Blockchain related errors"""
    
    def __init__(self, detail: str = "Blockchain operation failed"):
        super().__init__(detail, status.HTTP_502_BAD_GATEWAY)


class AIError(SatoshiSenseiException):
    """AI/ML related errors"""
    
    def __init__(self, detail: str = "AI processing failed"):
        super().__init__(detail, status.HTTP_500_INTERNAL_SERVER_ERROR)
