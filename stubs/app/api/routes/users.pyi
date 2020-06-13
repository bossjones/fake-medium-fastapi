from app.db.repositories.users import UsersRepository
from app.models.domain.users import User
from app.models.schemas.users import (
    UserInResponse,
    UserInUpdate,
)


async def retrieve_current_user(user: User = ...) -> UserInResponse: ...


async def update_current_user(
    user_update: UserInUpdate = ...,
    current_user: User = ...,
    users_repo: UsersRepository = ...
) -> UserInResponse: ...
