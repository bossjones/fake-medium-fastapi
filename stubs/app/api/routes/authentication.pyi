from app.db.repositories.users import UsersRepository
from app.models.schemas.users import (
    UserInCreate,
    UserInLogin,
    UserInResponse,
)


async def login(
    user_login: UserInLogin = ...,
    users_repo: UsersRepository = ...
) -> UserInResponse: ...


async def register(
    user_create: UserInCreate = ...,
    users_repo: UsersRepository = ...
) -> UserInResponse: ...
