from app.models.domain.users import UserInDB
from asyncpg.pool import Pool
from fastapi.applications import FastAPI
from httpx._client import AsyncClient


async def test_unregistered_user_will_receive_profile_without_following(
    app: FastAPI,
    client: AsyncClient,
    test_user: UserInDB
) -> None: ...


async def test_user_can_change_following_for_another_user(
    app: FastAPI,
    authorized_client: AsyncClient,
    pool: Pool,
    test_user: UserInDB,
    api_method: str,
    route_name: str,
    following: bool
) -> None: ...


async def test_user_can_not_change_following_state_for_him_self(
    app: FastAPI,
    authorized_client: AsyncClient,
    test_user: UserInDB,
    api_method: str,
    route_name: str
) -> None: ...


async def test_user_can_not_change_following_state_to_the_same_twice(
    app: FastAPI,
    authorized_client: AsyncClient,
    pool: Pool,
    test_user: UserInDB,
    api_method: str,
    route_name: str,
    following: bool
) -> None: ...


async def test_user_can_not_retrieve_not_existing_profile(
    app: FastAPI,
    authorized_client: AsyncClient,
    api_method: str,
    route_name: str
) -> None: ...


async def test_user_that_does_not_follows_another_will_receive_profile_without_follow(
    app: FastAPI,
    authorized_client: AsyncClient,
    pool: Pool
) -> None: ...


async def test_user_that_follows_another_will_receive_profile_with_follow(
    app: FastAPI,
    authorized_client: AsyncClient,
    pool: Pool,
    test_user: UserInDB
) -> None: ...
