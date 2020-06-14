import uuid
import warnings
from os import environ, getenv
from typing import AsyncGenerator

import alembic.config

# import docker as libdocker
import pytest
from asgi_lifespan import LifespanManager
from asyncpg.pool import Pool
from fastapi import FastAPI
from httpx import AsyncClient

from app.db.repositories.articles import ArticlesRepository
from app.db.repositories.users import UsersRepository
from app.models.domain.articles import Article
from app.models.domain.users import UserInDB
from app.services import jwt

# from tests.testing_helpers import ping_postgres, pull_image
from tests.testing_helpers import ping_postgres

# from fastapi.applications import FastAPI
# from httpx._client import AsyncClient

POSTGRES_DOCKER_IMAGE = "postgres:11.4-alpine"

USE_LOCAL_DB = bool(getenv("USE_LOCAL_DB_FOR_TEST", False))

# DOCKER_HOST = environ.get("DOCKER_HOST")
# DOCKER_TLS_VERIFY = environ.get("DOCKER_TLS_VERIFY", False)

POSTGRES_DB = environ.get("POSTGRES_DB", "rwdb")
POSTGRES_PORT = environ.get("POSTGRES_PORT", "5432")
POSTGRES_USER = environ.get("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = environ.get("POSTGRES_PASSWORD", "postgres")
POSTGRES_HOST = environ.get("POSTGRES_HOST", "172.16.2.234")

# tcp://127.0.0.1:1234
# DOCKER_TLS_VERIFY=1
# DOCKER_HOST=tcp://172.16.2.234:2376
# DOCKER_CERT_PATH=/Users/malcolm/.docker/machine/machines/dev2
# DOCKER_MACHINE_NAME=dev2

# @pytest.fixture(scope="session")
# def docker() -> libdocker.APIClient:
#     with libdocker.APIClient(version="auto", base_url=DOCKER_HOST) as client:
#         yield client


@pytest.fixture(scope="session", autouse=True)
# def postgres_server(docker: libdocker.APIClient) -> None:
def postgres_server() -> None:
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    dsn = f"postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/postgres"
    ping_postgres(dsn)
    environ["DB_CONNECTION"] = dsn

    # if not USE_LOCAL_DB:  # pragma: no cover
    #     pull_image(docker, POSTGRES_DOCKER_IMAGE)

    #     container = docker.create_container(
    #         image=POSTGRES_DOCKER_IMAGE,
    #         name="test-postgres-{}".format(uuid.uuid4()),
    #         detach=True,
    #     )
    #     docker.start(container=container["Id"])
    #     inspection = docker.inspect_container(container["Id"])
    #     host = inspection["NetworkSettings"]["IPAddress"]

    #     dsn = f"postgres://postgres:postgres@{host}/postgres"
    #     DB_CONNECTION=postgresql://postgres:postgres@172.16.2.234:5432/rwdb

    #     try:
    #         ping_postgres(dsn)
    #         environ["DB_CONNECTION"] = dsn

    #         yield container
    #     finally:
    #         docker.kill(container["Id"])
    #         docker.remove_container(container["Id"])
    # else:  # pragma: no cover
    #     yield
    #     return


@pytest.fixture(autouse=True)
async def apply_migrations(postgres_server: None) -> AsyncGenerator:
    alembic.config.main(argv=["upgrade", "head"])
    yield
    alembic.config.main(argv=["downgrade", "base"])


@pytest.fixture
def app(apply_migrations: None) -> FastAPI:
    from app.main import get_application  # local import for testing purpose

    return get_application()


@pytest.fixture
async def initialized_app(app: FastAPI) -> FastAPI:
    async with LifespanManager(app):
        yield app


@pytest.fixture
def pool(initialized_app: FastAPI) -> Pool:
    return initialized_app.state.pool


@pytest.fixture
async def client(initialized_app: FastAPI) -> AsyncClient:
    async with AsyncClient(
        app=initialized_app,
        base_url="http://testserver",
        headers={"Content-Type": "application/json"},
    ) as client:
        yield client


@pytest.fixture
def authorization_prefix() -> str:
    from app.core.config import JWT_TOKEN_PREFIX

    return JWT_TOKEN_PREFIX


@pytest.fixture
async def test_user(pool: Pool) -> UserInDB:
    async with pool.acquire() as conn:
        return await UsersRepository(conn).create_user(
            email="test@test.com", password="password", username="username"
        )


@pytest.fixture
async def test_article(test_user: UserInDB, pool: Pool) -> Article:
    async with pool.acquire() as connection:
        articles_repo = ArticlesRepository(connection)
        return await articles_repo.create_article(
            slug="test-slug",
            title="Test Slug",
            description="Slug for tests",
            body="Test " * 100,
            author=test_user,
            tags=["tests", "testing", "pytest"],
        )


@pytest.fixture
def token(test_user: UserInDB) -> str:
    return jwt.create_access_token_for_user(test_user, environ["SECRET_KEY"])


@pytest.fixture
def authorized_client(
    client: AsyncClient, token: str, authorization_prefix: str
) -> AsyncClient:
    client.headers = {
        "Authorization": f"{authorization_prefix} {token}",
        **client.headers,
    }  # type: ignore
    return client
