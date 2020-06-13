from app.models.domain.articles import Article
from asyncpg.pool import Pool
from fastapi.applications import FastAPI
from httpx._client import AsyncClient


async def test_user_can_add_comment_for_article(
    app: FastAPI,
    authorized_client: AsyncClient,
    test_article: Article
) -> None: ...


async def test_user_can_delete_own_comment(
    app: FastAPI,
    authorized_client: AsyncClient,
    test_article: Article
) -> None: ...


async def test_user_can_not_delete_not_authored_comment(
    app: FastAPI,
    authorized_client: AsyncClient,
    test_article: Article,
    pool: Pool
) -> None: ...


async def test_user_will_receive_error_for_not_existing_comment(
    app: FastAPI,
    authorized_client: AsyncClient,
    test_article: Article
) -> None: ...
