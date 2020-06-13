from app.db.repositories.comments import CommentsRepository
from app.models.domain.articles import Article
from app.models.domain.comments import Comment
from app.models.domain.users import User
from app.models.schemas.comments import (
    CommentInCreate,
    CommentInResponse,
    ListOfCommentsInResponse,
)
from typing import Optional


async def create_comment_for_article(
    comment_create: CommentInCreate = ...,
    article: Article = ...,
    user: User = ...,
    comments_repo: CommentsRepository = ...
) -> CommentInResponse: ...


async def delete_comment_from_article(
    comment: Comment = ...,
    comments_repo: CommentsRepository = ...
) -> None: ...


async def list_comments_for_article(
    article: Article = ...,
    user: Optional[User] = ...,
    comments_repo: CommentsRepository = ...
) -> ListOfCommentsInResponse: ...
