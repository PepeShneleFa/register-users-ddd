from authx import AuthX, AuthXConfig

from datetime import datetime, timedelta
from typing import Optional

from src.infrastructure.log.logger import logger
from src.domain.protocols.authx_service_protocol import AuthxServiceProtocol

#service for creating JWT tokens
class AuthxService(AuthxServiceProtocol):
    def __init__(self) -> None:
        self._config: Optional[AuthXConfig] = None
        self._authx: Optional[AuthX] = None
    
    @property
    def config(self) -> AuthXConfig:
        if self._config is None:
            """config with service settings"""
            try:
                self._config = AuthXConfig()
                self._config.JWT_ALGORITHM = "HS256"
                self._config.JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=3)
                self._config.JWT_TOKEN_LOCATION = ["headers"]
                self._config.JWT_SECRET_KEY = "SECRET_KEY"
                logger.info("AuthxService initialized")
            except Exception as e:
                logger.exception(f"Error in AuthxService initialization: {e}")
                raise
        return self._config
    
    @property
    def authx(self) -> AuthX:
        if self._authx is None:
            """authx service creation config"""
            try:
                self._authx = AuthX(
                    config=self.config,
                )
                logger.info("Authx instance initialized")
            except Exception as e:
                logger.exception(f"Error in Authx initialization: {e}")
                raise
        return self._authx
    
    #function to create a JWT token
    def create_access_token(self, uid: str) -> str:
        try:
            return self.authx.create_access_token(
                uid=uid
            )
        except Exception as e:
            logger.exception(f"Error in creating token: {e}")
            raise