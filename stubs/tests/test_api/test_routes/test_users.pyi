from _pytest.fixtures import SubRequest
from app.models.domain.users import UserInDB
from asyncpg.pool import Pool
from fastapi.applications import FastAPI
from httpx._client import AsyncClient


async def test_user_can_change_password(
    app: FastAPI,
    authorized_client: AsyncClient,
    test_user: UserInDB,
    token: str,
    pool: Pool
) -> None: ...


async def test_user_can_not_access_own_profile_if_not_logged_in(
    app: FastAPI,
    client: AsyncClient,
    test_user: UserInDB,
    api_method: str,
    route_name: str
) -> None: ...


async def test_user_can_not_retrieve_own_profile_if_wrong_token(
    app: FastAPI,
    client: AsyncClient,
    test_user: UserInDB,
    api_method: str,
    route_name: str,
    wrong_authorization_header: str
) -> None: ...


async def test_user_can_not_take_already_used_credentials(
    app: FastAPI,
    authorized_client: AsyncClient,
    pool: Pool,
    token: str,
    credentials_part: str,
    credentials_value: str
) -> None: ...


async def test_user_can_retrieve_own_profile(
    app: FastAPI,
    authorized_client: AsyncClient,
    test_user: UserInDB,
    token: str
) -> None: ...


async def test_user_can_update_own_profile(
    app: FastAPI,
    authorized_client: AsyncClient,
    test_user: UserInDB,
    token: str,
    update_value: str,
    update_field: str
) -> None: ...


def wrong_authorization_header(request: SubRequest) -> str: ...
