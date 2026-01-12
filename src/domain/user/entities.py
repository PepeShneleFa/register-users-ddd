from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List

from src.domain.protocols.argon_config_protocol import ArgonConfigProtocol
from src.domain.user.value_object import UserID, Name, Hash, NameProfile, Age, City, Title, Content, Status
from src.domain.events.domain_event import DomainEvent
from src.domain.events.events import UserRegisteredEvent, UserProfileRegisteredEvent, PostRegisteredEvent

@dataclass(frozen=True, slots=True)
class User:
    username: Name
    user_id: UserID
    password: Hash

    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    _events: List["DomainEvent"] = field(default_factory=list, repr=False, init=False)

    @classmethod
    def register(cls, raw_username: str, plain_password: str, hasher: ArgonConfigProtocol) -> "User":
        username = Name.create(raw_username)
        user_id = UserID.generate()
        password = Hash.for_plain(plain_password, hasher)

        user = object.__new__(cls)
        object.__setattr__(user, "username", username)
        object.__setattr__(user, "user_id", user_id)
        object.__setattr__(user, "password", password)
        object.__setattr__(user, "created_at", datetime.now(timezone.utc))
        object.__setattr__(user, "_events", [UserRegisteredEvent(user_id=user_id, username=username)])
        return user

    def pull_events(self) -> List["DomainEvent"]:
        event = self._events.copy()
        object.__setattr__(self, "_events", [])
        return event

@dataclass(frozen=True, slots=True)
class Profile:
    user_id: UserID
    age: Age
    name: NameProfile
    city: City

    _events: List["DomainEvent"] = field(default_factory=list, repr=False, init=False)

    @classmethod
    def create(cls, user_id: UserID, age: int, name: str, city: str) -> "Profile":
        profile_age = Age.create(age)
        profile_name = NameProfile.create(name)
        profile_city = City.create(city)

        user = object.__new__(cls)
        object.__setattr__(user, "user_id", user_id)
        object.__setattr__(user, "age", profile_age)
        object.__setattr__(user, "name", profile_name)
        object.__setattr__(user, "city", profile_city)
        object.__setattr__(user, "_events", [UserProfileRegisteredEvent(user_id=user_id)])
        return user
    
    def pull_events(self) -> List["DomainEvent"]:
        event = self._events.copy()
        object.__setattr__(self, "_events", [])
        return event

@dataclass(frozen=True, slots=True)
class Posts:
    user_id: UserID
    post_id: UserID
    title: Title
    content: Content
    status: Status
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    _events: List["DomainEvent"] = field(default_factory=list, repr=False, init=False)

    @classmethod
    def create(cls, post_title: str, post_content: str, user_id: UserID) -> "Posts":
        post_id = UserID.generate()
        title = Title.create(post_title)
        content = Content.create(post_content)
        status = Status.draft()

        post = object.__new__(cls)
        object.__setattr__(post, "user_id", user_id)
        object.__setattr__(post, "post_id", post_id)
        object.__setattr__(post, "title", title)
        object.__setattr__(post, "content", content)
        object.__setattr__(post, "status", status)
        object.__setattr__(post, "created_at", datetime.now(timezone.utc))
        object.__setattr__(post, "_events", [PostRegisteredEvent(user_id=user_id, post_id=post_id)])
        return post
    
    def pull_events(self) -> List["DomainEvent"]:
        event = self._events.copy()
        object.__setattr__(self, "_events", [])
        return event
