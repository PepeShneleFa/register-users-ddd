from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from typing import Annotated

from src.infrastructure.db.models import UserPosts
from src.application.auth.commands import UserRegisteredCommand, ProfileRegisteredCommand, PostRegisteredcommand
from src.presentation.schemas.user import AuthResult, UserAuthRequest, ProfileAuthRequest, ProfileAuthResult, PostAuthResult, PostAuthRequest, GetPostsByID
from src.application.auth.handle import RegisterUserHandle
from src.presentation.api.deps import get_register_user_handle, get_current_user_id, get_user_repository

from src.infrastructure.db.repository.user_repository import UserRepository

http_bearer = HTTPBearer()
router = APIRouter(
    prefix="/auth"
)

#endpoint for adding a user
@router.post("/add-user", status_code=status.HTTP_201_CREATED, response_model=AuthResult)
async def add_user_handler(
    request: UserAuthRequest,
    handle: Annotated[RegisterUserHandle, Depends(get_register_user_handle)],
) -> AuthResult:
    try:
        user = await handle.handle(
            cmd=UserRegisteredCommand(
                username=request.username,
                password=request.password,
            )
        )
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to register the user: {e}"
        )

#endpoint for adding a profile
@router.post("/add-profile", status_code=status.HTTP_201_CREATED, response_model=ProfileAuthResult)
async def add_profile_handler(
    request: ProfileAuthRequest,
    _: Annotated[HTTPAuthorizationCredentials, Depends(http_bearer)],
    handle: Annotated[RegisterUserHandle, Depends(get_register_user_handle)],
    user_id: Annotated[str, Depends(get_current_user_id)],
) -> ProfileAuthResult:
    try:
        profile = await handle.profile_handle(
            cmd=ProfileRegisteredCommand(
                age=request.age,
                name=request.name,
                city=request.city,
            ),
            user_id=user_id,
        )
        return profile
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to register the profile: {e}",
        )

#endpoint for adding a post to the user
@router.post("/add-post", status_code=status.HTTP_201_CREATED, response_model=PostAuthResult)
async def add_post_handler(
    request: PostAuthRequest,
    handle: Annotated[RegisterUserHandle, Depends(get_register_user_handle)],
    user_id: Annotated[str, Depends(get_current_user_id)],
    _: Annotated[HTTPAuthorizationCredentials, Depends(http_bearer)],
) -> PostAuthResult:
    try:
        post = await handle.posts_handle(
            cmd=PostRegisteredcommand(
                title=request.title,
                content=request.content,
            ),
            user_id=user_id
        )
        return post
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to register the profile: {e}",
        )

#endpoint for receiving user posts by ID
@router.get("/get-user-posts-by-id", status_code=status.HTTP_200_OK)
async def get_user_posts_by_id_handler(
    repo: Annotated[UserRepository, Depends(get_user_repository)],
    user_id: Annotated[str, Depends(get_current_user_id)],
    _: Annotated[HTTPAuthorizationCredentials, Depends(http_bearer)],
):
    try:
        posts = await repo.get_user_post_by_id(user_id)
        return posts
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to register the profile: {e}",
        )