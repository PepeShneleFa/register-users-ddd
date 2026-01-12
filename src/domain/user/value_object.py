from dataclasses import dataclass, field
from uuid import uuid4, UUID

from src.domain.protocols.argon_config_protocol import ArgonConfigProtocol

@dataclass(frozen=True, slots=True)
class UserID:
    value: UUID = field(default_factory=uuid4)

    @classmethod
    def generate(cls) -> "UserID":
        return cls()

@dataclass(frozen=True, slots=True)
class Name:
    value: str

    def __post_init__(self) -> None:
        v = self.value.strip()
        if not v:
            raise ValueError("username cannot be empty")
        if len(v) < 8:
            raise ValueError("username is too short")
        if len(v) > 15:
            raise ValueError("username is too long")
        object.__setattr__(self, "value", v)
    
    @classmethod
    def create(cls, raw: str) -> "Name":
        return cls(raw)

@dataclass(frozen=True, slots=True)
class Hash:
    value: str

    @classmethod
    def for_plain(cls, plain_password: str, hasher: ArgonConfigProtocol) -> "Hash":
        if len(plain_password) < 5:
            raise ValueError("The password must not be less than 5 characters long.")
        if len(plain_password) > 15:
            raise ValueError("The password must not be longer than 15 characters.")
        return cls(hasher.hash(plain_password))
    
    def verify(cls, plain_password: str, hasher: ArgonConfigProtocol) -> bool:
        return hasher.verify(cls.value, plain_password)

@dataclass(frozen=True, slots=True)
class NameProfile:
    value: str

    def __post_init__(self) -> None:
        v = self.value.strip()
        if not v:
            raise ValueError("name cannot be empty")
        if len(v) < 3:
            raise ValueError("name is too short")
        if len(v) > 10:
            raise ValueError("name is too long")
        object.__setattr__(self, "value", v)
    
    @classmethod
    def create(cls, name: str) -> "NameProfile":
        return cls(name)

@dataclass(frozen=True, slots=True)
class Age:
    value: int

    def __post_init__(self) -> None:
        v = self.value
        if not isinstance(self.value, int):
            raise ValueError("Age must be int")
        if v <= 0:
            raise ValueError("age cannot be less than 0")
        if v >= 80:
            raise ValueError("age cannot be more than 80")
        object.__setattr__(self, "value", v)
    
    @classmethod
    def create(cls, age: int) -> "Age":
        return cls(age)

@dataclass(frozen=True, slots=True)
class City:
    value: str

    def __post_init__(self) -> None:
        v = self.value.strip()
        if not isinstance(v, str):
            raise TypeError("City must be str")
        if len(v) < 1:
            raise ValueError("city is too short")
        if len(v) > 10:
            raise ValueError("city is too long")
        object.__setattr__(self, "value", v)
    
    @classmethod
    def create(cls, city: str) -> "City":
        return cls(city)

@dataclass(frozen=True, slots=True)
class Title:
    value: str

    def __post_init__(self) -> None:
        v = self.value.strip()
        if not isinstance(v, str):
            raise ValueError("Title must be str")
        if len(v) < 3:
            raise ValueError("Title is too short")
        if len(v) > 25:
            raise ValueError("Title is too long")
        object.__setattr__(self, "value", v)
    
    @classmethod
    def create(cls, title: str) -> "Title":
        return cls(title)

@dataclass(frozen=True, slots=True)
class Content:
    value: str

    def __post_init__(self) -> None:
        v = self.value.strip()
        if not isinstance(v, str):
            raise ValueError("Content must be str")
        if len(v) < 3:
            raise ValueError("Content is to short")
        if len(v) > 255:
            raise ValueError("Content is to long")
        object.__setattr__(self, "value", v)
    
    @classmethod
    def create(cls, content: str) -> "Content":
        return cls(content)

@dataclass(frozen=True, slots=True)
class Status:
    value: str

    @classmethod
    def draft(cls) -> "Status":
        return cls("draft")
    
    @classmethod
    def published(cls) -> "Status":
        return cls("published")
    
    @classmethod
    def archived(cls) -> "Status":
        return cls("archived")
    
    def __post_init__(self) -> None:
        if self.value not in {"draft", "published", "archived"}:
            raise ValueError(f"Invalid status: {self.value}")