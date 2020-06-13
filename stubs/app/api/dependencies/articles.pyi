from app.db.repositories.articles import ArticlesRepository
from app.models.domain.articles import Article
from app.models.domain.users import User
from typing import Optional


async def get_article_by_slug_from_path(
    slug: str = ...,
    user: Optional[User] = ...,
    articles_repo: ArticlesRepository = ...
) -> Article: ...
