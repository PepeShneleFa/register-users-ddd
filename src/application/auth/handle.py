from src.application.auth.commands import UserRegisteredCommand, ProfileRegisteredCommand, PostRegisteredcommand
from src.application.auth.dto import AuthResultDTO, AuthProfileResultDTO, AuthPostResultDTO

from src.domain.user.value_object import UserID
from src.domain.protocols.authx_service_protocol import AuthxServiceProtocol
from src.domain.protocols.argon_config_protocol import ArgonConfigProtocol
from src.domain.protocols.user_repository_protocol import UserRepositoryProtocol
from src.domain.user.entities import User, Profile, Posts

class RegisterUserHandle:
    def __init__(
            self,
            repo: UserRepositoryProtocol,
            authx: AuthxServiceProtocol,
            hasher: ArgonConfigProtocol,
    ) -> None:
        self._repo = repo
        self._authx = authx
        self._hasher = hasher
    
    async def handle(self, cmd: UserRegisteredCommand) -> AuthResultDTO:
        try:
            user = User.register(
                raw_username=cmd.username,
                plain_password=cmd.password,
                hasher=self._hasher,
            )
            await self._repo.add_user(user)

            access_token = self._authx.create_access_token(
                uid=str(user.user_id.value),
            )

            return AuthResultDTO(
                status="success",
                message="The account has been successfully registered!",
                access_token=access_token,
            )
        except Exception:
            raise
    
    async def profile_handle(self, cmd: ProfileRegisteredCommand, user_id: str) -> AuthProfileResultDTO:
        try:
            profile = Profile.create(
                user_id=UserID(user_id),
                age=cmd.age,
                name=cmd.name,
                city=cmd.city,
            )
            await self._repo.add_profile(profile)

            return AuthProfileResultDTO(
                status="success",
                message="Your profile has been successfully added!",
            )
        except Exception:
            raise
    
    async def posts_handle(self, cmd: PostRegisteredcommand, user_id: str) -> AuthProfileResultDTO:
        try:
            post = Posts.create(
                post_title=cmd.title,
                post_content=cmd.content,
                user_id=UserID(user_id),
            )
            await self._repo.add_post(post)

            return AuthPostResultDTO(
                status="success",
                message="Your post has been successfully added!",
            )
        except Exception:
            raise