from app.db.repositories.users import UsersRepository
from app.models.domain.users import User
from starlette.requests import Request
from typing import (
    Callable,
    Optional,
)


def _get_authorization_header_retriever(*, required: bool = ...) -> Callable: ...


async def _get_current_user(
    users_repo: UsersRepository = ...,
    token: str = ...
) -> User: ...


async def _get_current_user_optional(
    repo: UsersRepository = ...,
    token: str = ...
) -> Optional[User]: ...


def get_current_user_authorizer(*, required: bool = ...) -> Callable: ...


class RWAPIKeyHeader:
    async def __call__(self, request: Request) -> Optional[str]: ...
