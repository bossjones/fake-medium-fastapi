from app.models.domain.articles import Article
from app.models.domain.users import User
from asyncpg import Record
from asyncpg.connection import Connection
from typing import (
    List,
    Optional,
    Sequence,
)


class ArticlesRepository:
    def __init__(self, conn: Connection) -> None: ...
    async def _get_article_from_db_record(
        self,
        *,
        article_row: Record,
        slug: str,
        author_username: str,
        requested_user: Optional[User]
    ) -> Article: ...
    async def _link_article_with_tags(self, *, slug: str, tags: Sequence[str]) -> None: ...
    async def add_article_into_favorites(
        self,
        *,
        article: Article,
        user: User
    ) -> None: ...
    async def create_article(
        self,
        *,
        slug: str,
        title: str,
        description: str,
        body: str,
        author: User,
        tags: Optional[Sequence[str]] = ...
    ) -> Article: ...
    async def delete_article(self, *, article: Article) -> None: ...
    async def filter_articles(
        self,
        *,
        tag: Optional[str] = ...,
        author: Optional[str] = ...,
        favorited: Optional[str] = ...,
        limit: int = ...,
        offset: int = ...,
        requested_user: Optional[User] = ...
    ) -> List[Article]: ...
    async def get_article_by_slug(
        self,
        *,
        slug: str,
        requested_user: Optional[User] = ...
    ) -> Article: ...
    async def get_articles_for_user_feed(
        self,
        *,
        user: User,
        limit: int = ...,
        offset: int = ...
    ) -> List[Article]: ...
    async def get_favorites_count_for_article_by_slug(self, *, slug: str) -> int: ...
    async def get_tags_for_article_by_slug(self, *, slug: str) -> List[str]: ...
    async def is_article_favorited_by_user(self, *, slug: str, user: User) -> bool: ...
    async def remove_article_from_favorites(
        self,
        *,
        article: Article,
        user: User
    ) -> None: ...
    async def update_article(
        self,
        *,
        article: Article,
        slug: Optional[str] = ...,
        title: Optional[str] = ...,
        body: Optional[str] = ...,
        description: Optional[str] = ...
    ) -> Article: ...
