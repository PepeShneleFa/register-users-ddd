from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column
from sqlalchemy import String, Integer, ForeignKey, Text

from typing import List

from datetime import datetime

class Base(DeclarativeBase):
    pass

class UserModel(Base):
    __tablename__ = "user"

    username: Mapped[str] = mapped_column(
        String, unique=True, index=True,
    )
    user_id: Mapped[str] = mapped_column(
        String, primary_key=True, index=True,
        nullable=False
    )
    password: Mapped[str] = mapped_column(
        String, nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        nullable=False,
    )

    profile: Mapped["UserProfile"] = relationship(
        back_populates="user", uselist=False,
    )
    posts: Mapped[List["UserPosts"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

class UserProfile(Base):
    __tablename__ = "profile"

    user_id: Mapped[str] = mapped_column(
        ForeignKey("user.user_id"), primary_key=True, index=True,
    )
    age: Mapped[int] = mapped_column(
        Integer, nullable=False,
    )
    name: Mapped[str] = mapped_column(
        String, nullable=False,
    )
    city: Mapped[str] = mapped_column(
        String, nullable=False,
    )

    user: Mapped["UserModel"] = relationship(
        back_populates="profile", uselist=False,
    )

class UserPosts(Base):
    __tablename__ = "posts"

    user_id: Mapped[str] = mapped_column(
        ForeignKey("user.user_id", ondelete="CASCADE"),
        index=True, nullable=False,
    )
    post_id: Mapped[str] = mapped_column(
        String, primary_key=True, index=True,
        nullable=False,
    )
    title: Mapped[str] = mapped_column(
        String(25), nullable=False,
    )
    content: Mapped[str] = mapped_column(
        Text, nullable=False,
    )
    status: Mapped[str] = mapped_column(
        String(20), default="draft", nullable=False,
        index=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        nullable=False,
    )
    user: Mapped["UserModel"] = relationship(
        back_populates="posts",
    )

    