from app.models.domain.users import UserInDB
from asyncpg.pool import Pool
from fastapi.applications import FastAPI
from httpx._client import AsyncClient


async def test_failed_user_registration_when_some_credentials_are_taken(
    app: FastAPI,
    client: AsyncClient,
    test_user: UserInDB,
    credentials_part: str,
    credentials_value: str
) -> None: ...


async def test_user_success_registration(
    app: FastAPI,
    client: AsyncClient,
    pool: Pool
) -> None: ...
