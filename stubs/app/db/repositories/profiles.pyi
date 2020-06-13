from app.models.domain.profiles import Profile
from app.models.domain.users import User
from asyncpg.connection import Connection
from typing import (
    Optional,
    Union,
)


class ProfilesRepository:
    def __init__(self, conn: Connection) -> None: ...
    async def add_user_into_followers(
        self,
        *,
        target_user: Union[User, Profile],
        requested_user: Union[User, Profile]
    ) -> None: ...
    async def get_profile_by_username(
        self,
        *,
        username: str,
        requested_user: Optional[Union[User, Profile]]
    ) -> Profile: ...
    async def is_user_following_for_another_user(
        self,
        *,
        target_user: Union[User, Profile],
        requested_user: Union[User, Profile]
    ) -> bool: ...
    async def remove_user_from_followers(
        self,
        *,
        target_user: Union[User, Profile],
        requested_user: Union[User, Profile]
    ) -> None: ...
