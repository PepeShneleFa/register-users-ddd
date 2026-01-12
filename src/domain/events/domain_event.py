from dataclasses import dataclass, field
from abc import ABC, abstractmethod

from typing import Dict, Any

from datetime import datetime, timezone
from uuid import uuid4, UUID

@dataclass(frozen=True, slots=True)
class DomainEvent(ABC):
    event_id: UUID = field(default_factory=uuid4)
    occurred_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @abstractmethod
    def payload(self) -> Dict[str, Any]:
        ...
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_id": str(self.event_id),
            "event_type": self.__class__.__name__,
            "occurred_at": self.occurred_at.isoformat(),
            "data": self.payload()
        }