from asyncpg.pool import Pool
from fastapi.applications import FastAPI
from httpx._client import AsyncClient


async def test_empty_list_when_no_tags_exist(
    app: FastAPI,
    client: AsyncClient
) -> None: ...


async def test_list_of_tags_when_tags_exist(
    app: FastAPI,
    client: AsyncClient,
    pool: Pool
) -> None: ...
