from app.models.domain.users import UserInDB
from fastapi.applications import FastAPI
from httpx._client import AsyncClient


async def test_user_login_when_credential_part_does_not_match(
    app: FastAPI,
    client: AsyncClient,
    test_user: UserInDB,
    credentials_part: str,
    credentials_value: str
) -> None: ...


async def test_user_successful_login(
    app: FastAPI,
    client: AsyncClient,
    test_user: UserInDB
) -> None: ...
