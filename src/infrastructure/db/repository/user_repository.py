from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy import insert, select

from typing import Optional

from src.infrastructure.log.logger import logger
from src.infrastructure.db.models import UserModel, UserProfile, UserPosts
from src.domain.user.entities import User, Profile, Posts
from src.domain.protocols.user_repository_protocol import UserRepositoryProtocol

class UserRepository(UserRepositoryProtocol):
    def __init__(
            self,
            async_factory: async_sessionmaker[AsyncSession],
    ) -> None:
        self._async_factory = async_factory
    
    async def add_user(self, user: User) -> None:
        try:
            async with self._async_factory() as session:
                stmt = insert(UserModel).values({
                    "username": user.username.value,
                    "user_id": str(user.user_id.value),
                    "password": user.password.value,
                    "created_at": user.created_at,
                })
                await session.execute(stmt)
                await session.commit()
                logger.info("the data is successfully populated into the database")
        except Exception as e:
            logger.exception(f"SQLAlchemy database error: {e}")
            raise
    
    async def add_profile(self, profile: Profile) -> None:
        try:
            async with self._async_factory() as session:
                stmt = insert(UserProfile).values({
                    "user_id": str(profile.user_id.value),
                    "age": profile.age.value,
                    "name": profile.name.value,
                    "city": profile.city.value,
                })
                await session.execute(stmt)
                await session.commit()
                logger.info(f"User profile '{str(profile.user_id.value)}' was successfully added!")
        except Exception as e:
            logger.exception(f"SQLAlchemy database error: {e}")
            raise
    
    async def add_post(self, post: Posts) -> None:
        try:
            async with self._async_factory() as session:
                stmt = insert(UserPosts).values({
                    "user_id": str(post.user_id.value),
                    "post_id": str(post.post_id.value),
                    "title": post.title.value,
                    "content": post.content.value,
                    "status": post.status.value,
                    "created_at": post.created_at,
                })
                await session.execute(stmt)
                await session.commit()
                logger.info(f"User post '{str(post.user_id.value)}' was successfully added!")
        except Exception as e:
            logger.exception(f"SQLAlchemy database error: {e}")
            raise
    
    async def get_user_post_by_id(self, user_id: str) -> list[UserPosts]:
        try:
            async with self._async_factory() as session:
                posts = await session.execute(
                    select(UserPosts).where(UserPosts.user_id == user_id)
                )
                result = posts.scalars().all()
                if not result:
                    return []
                
                return result
        except Exception as e:
            logger.exception(f"SQLAlchemy database error: {e}")
            raise