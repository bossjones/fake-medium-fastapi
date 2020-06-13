from fastapi.applications import FastAPI
from httpx._client import AsyncClient


async def test_unable_to_login_when_user_does_not_exist_any_more(
    app: FastAPI,
    client: AsyncClient,
    authorization_prefix: str
) -> None: ...


async def test_unable_to_login_with_wrong_jwt_prefix(
    app: FastAPI,
    client: AsyncClient,
    token: str
) -> None: ...
