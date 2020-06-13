from app.models.domain.articles import Article
from app.models.domain.comments import Comment
from app.models.domain.users import User
from asyncpg import Record
from asyncpg.connection import Connection
from typing import (
    List,
    Optional,
)


class CommentsRepository:
    def __init__(self, conn: Connection) -> None: ...
    async def _get_comment_from_db_record(
        self,
        *,
        comment_row: Record,
        author_username: str,
        requested_user: Optional[User]
    ) -> Comment: ...
    async def create_comment_for_article(
        self,
        *,
        body: str,
        article: Article,
        user: User
    ) -> Comment: ...
    async def delete_comment(self, *, comment: Comment) -> None: ...
    async def get_comment_by_id(
        self,
        *,
        comment_id: int,
        article: Article,
        user: Optional[User] = ...
    ) -> Comment: ...
    async def get_comments_for_article(
        self,
        *,
        article: Article,
        user: Optional[User] = ...
    ) -> List[Comment]: ...
