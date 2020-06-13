from app.models.domain.articles import Article
from app.models.domain.users import UserInDB
from asyncpg.pool import Pool
from fastapi.applications import FastAPI
from httpx._client import AsyncClient


def app(apply_migrations: None) -> FastAPI: ...


def authorization_prefix() -> str: ...


def authorized_client(
    client: AsyncClient,
    token: str,
    authorization_prefix: str
) -> AsyncClient: ...


def initialized_app(app: FastAPI) -> FastAPI: ...


def pool(initialized_app: FastAPI) -> Pool: ...


def postgres_server() -> None: ...


async def test_article(
    test_user: UserInDB,
    pool: Pool
) -> Article: ...


async def test_user(pool: Pool) -> UserInDB: ...


def token(test_user: UserInDB) -> str: ...
