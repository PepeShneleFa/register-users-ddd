from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from typing import Optional

from src.infrastructure.log.logger import logger
from src.domain.protocols.argon_config_protocol import ArgonConfigProtocol

class ArgonHashConfig(ArgonConfigProtocol):
    def __init__(self) -> None:
        self._ph: Optional[PasswordHasher] = None
    
    @property
    def ph(self) -> PasswordHasher:
        if self._ph is None:
            try:
                self._ph = PasswordHasher(
                    time_cost=4, parallelism=4,
                    hash_len=32, salt_len=16,
                    memory_cost=102400,
                )
            except Exception as e:
                logger.exception("error in init argon-ph")
                raise
        return self._ph
    
    def hash(self, password: str) -> str:
        return self.ph.hash(password)
    
    def verify(self, hashed: str, password: str) -> bool:
        try:
            return self.ph.verify(
                hashed, password,
            )
        except VerifyMismatchError:
            return False