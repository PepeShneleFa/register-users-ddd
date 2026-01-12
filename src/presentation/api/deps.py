from src.infrastructure.db.session import DataBaseConfig
from src.infrastructure.security.argon_config import ArgonHashConfig
from src.infrastructure.security.authx_config import AuthxService
from src.infrastructure.db.repository.user_repository import UserRepository
from src.application.auth.handle import RegisterUserHandle

from authx import TokenPayload
from fastapi import Depends, HTTPException, status

from typing import Annotated
from functools import lru_cache

@lru_cache(maxsize=1)
def get_db_config() -> DataBaseConfig:
    """Singleton database configuration"""
    return DataBaseConfig()

@lru_cache(maxsize=1)
def get_argon_config() -> ArgonHashConfig:
    """Singleton password hasher configuration"""
    return ArgonHashConfig()

@lru_cache(maxsize=1)
def get_authx_service() -> AuthxService:
    """Singleton authx service configuration"""
    return AuthxService()

def get_user_repository(
    db: Annotated[DataBaseConfig, Depends(get_db_config)],
) -> UserRepository:
    """User repository with database session dependency"""
    return UserRepository(db.async_session)

def get_register_user_handle(
    repo: Annotated[UserRepository, Depends(get_user_repository)],
    hasher: Annotated[ArgonHashConfig, Depends(get_argon_config)],
    authx: Annotated[AuthxService, Depends(get_authx_service)],
) -> RegisterUserHandle:
    """Register user handler with all required dependencies"""
    return RegisterUserHandle(
        repo=repo, authx=authx, hasher=hasher,
    )

def get_current_user_id(
    payload: Annotated[TokenPayload, Depends(get_authx_service().authx.access_token_required)],
) -> str:
    """Extract current user identifier from JWT patload."""
    if payload.sub is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )
    return str(payload.sub) 