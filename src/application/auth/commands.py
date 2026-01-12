from dataclasses import dataclass

@dataclass(frozen=True)
class UserRegisteredCommand:
    username: str
    password: str

@dataclass(frozen=True)
class ProfileRegisteredCommand:
    age: int
    name: str
    city: str

@dataclass(frozen=True)
class PostRegisteredcommand:
    title: str
    content: str

@dataclass(frozen=True)
class PostsGetCommand:
    user_id: str