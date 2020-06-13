from app.models.domain.users import (
    User,
    UserInDB,
)
from typing import Optional


class UsersRepository:
    async def create_user(self, *, username: str, email: str, password: str) -> UserInDB: ...
    async def get_user_by_email(self, *, email: str) -> UserInDB: ...
    async def get_user_by_username(self, *, username: str) -> UserInDB: ...
    async def update_user(
        self,
        *,
        user: User,
        username: Optional[str] = ...,
        email: Optional[str] = ...,
        password: Optional[str] = ...,
        bio: Optional[str] = ...,
        image: Optional[str] = ...
    ) -> UserInDB: ...
