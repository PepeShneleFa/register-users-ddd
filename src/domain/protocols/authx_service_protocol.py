from typing import Protocol

class AuthxServiceProtocol(Protocol):
    def create_access_token(self, uid: str) -> str: ...