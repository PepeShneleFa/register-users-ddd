from dataclasses import dataclass

from src.domain.events.domain_event import DomainEvent
from src.domain.user.value_object import UserID, Name

@dataclass(frozen=True, slots=True, kw_only=True)
class UserRegisteredEvent(DomainEvent):
    user_id: UserID
    username: Name

    def payload(self) -> dict:
        return {"user_id": str(self.user_id.value), "username": self.username.value}

@dataclass(frozen=True, slots=True, kw_only=True)
class UserProfileRegisteredEvent(DomainEvent):
    user_id: UserID

    def payload(self) -> dict:
        return {"user_id": str(self.user_id.value)}

@dataclass(frozen=True, slots=True, kw_only=True)
class PostRegisteredEvent(DomainEvent):
    user_id: UserID
    post_id: UserID

    def payload(self) -> dict:
        return {"user_id": str(self.user_id.value), "post_id": str(self.post_id.value)}