from app.db.repositories.comments import CommentsRepository
from app.models.domain.articles import Article
from app.models.domain.comments import Comment
from app.models.domain.users import User
from typing import Optional


async def get_comment_by_id_from_path(
    comment_id: int = ...,
    article: Article = ...,
    user: Optional[User] = ...,
    comments_repo: CommentsRepository = ...
) -> Comment: ...
