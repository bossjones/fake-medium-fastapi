from app.models.domain.articles import Article
from app.models.domain.users import UserInDB
from asyncpg.pool import Pool
from fastapi.applications import FastAPI
from httpx._client import AsyncClient


async def test_article_will_contain_only_attached_tags(
    app: FastAPI,
    authorized_client: AsyncClient,
    test_user: UserInDB,
    pool: Pool
) -> None: ...


async def test_empty_feed_if_user_has_not_followings(
    app: FastAPI,
    authorized_client: AsyncClient,
    test_article: Article,
    test_user: UserInDB,
    pool: Pool
) -> None: ...


async def test_filtering_by_authors(
    app: FastAPI,
    authorized_client: AsyncClient,
    test_user: UserInDB,
    pool: Pool,
    author: str,
    result: int
) -> None: ...


async def test_filtering_by_favorited(
    app: FastAPI,
    authorized_client: AsyncClient,
    test_user: UserInDB,
    pool: Pool,
    favorited: str,
    result: int
) -> None: ...


async def test_filtering_by_tags(
    app: FastAPI,
    authorized_client: AsyncClient,
    test_user: UserInDB,
    pool: Pool,
    tag: str,
    result: int
) -> None: ...


async def test_filtering_with_limit_and_offset(
    app: FastAPI,
    authorized_client: AsyncClient,
    test_user: UserInDB,
    pool: Pool
) -> None: ...


async def test_not_existing_tags_will_be_created_without_duplication(
    app: FastAPI,
    authorized_client: AsyncClient,
    test_user: UserInDB
) -> None: ...


async def test_user_can_change_favorite_state(
    app: FastAPI,
    authorized_client: AsyncClient,
    test_article: Article,
    test_user: UserInDB,
    pool: Pool,
    api_method: str,
    route_name: str,
    favorite_state: bool
) -> None: ...


async def test_user_can_create_article(
    app: FastAPI,
    authorized_client: AsyncClient,
    test_user: UserInDB
) -> None: ...


async def test_user_can_delete_his_article(
    app: FastAPI,
    authorized_client: AsyncClient,
    test_article: Article,
    pool: Pool
) -> None: ...


async def test_user_can_not_change_article_state_twice(
    app: FastAPI,
    authorized_client: AsyncClient,
    test_article: Article,
    test_user: UserInDB,
    pool: Pool,
    api_method: str,
    route_name: str,
    favorite_state: bool
) -> None: ...


async def test_user_can_not_create_article_with_duplicated_slug(
    app: FastAPI,
    authorized_client: AsyncClient,
    test_article: Article
) -> None: ...


async def test_user_can_not_modify_article_that_is_not_authored_by_him(
    app: FastAPI,
    authorized_client: AsyncClient,
    pool: Pool,
    api_method: str,
    route_name: str
) -> None: ...


async def test_user_can_not_retrieve_not_existing_article(
    app: FastAPI,
    authorized_client: AsyncClient,
    test_article: Article,
    api_method: str,
    route_name: str
) -> None: ...


async def test_user_can_retrieve_article_if_exists(
    app: FastAPI,
    authorized_client: AsyncClient,
    test_article: Article
) -> None: ...


async def test_user_can_update_article(
    app: FastAPI,
    authorized_client: AsyncClient,
    test_article: Article,
    update_field: str,
    update_value: str,
    extra_updates: dict
) -> None: ...


async def test_user_receiving_feed_with_limit_and_offset(
    app: FastAPI,
    authorized_client: AsyncClient,
    test_article: Article,
    test_user: UserInDB,
    pool: Pool
) -> None: ...


async def test_user_will_receive_only_following_articles(
    app: FastAPI,
    authorized_client: AsyncClient,
    test_article: Article,
    test_user: UserInDB,
    pool: Pool
) -> None: ...
