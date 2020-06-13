from app.db.repositories.articles import ArticlesRepository
from app.models.domain.articles import Article
from app.models.domain.users import User
from app.models.schemas.articles import (
    ArticleInResponse,
    ListOfArticlesInResponse,
)


async def get_articles_for_user_feed(
    limit: int = ...,
    offset: int = ...,
    user: User = ...,
    articles_repo: ArticlesRepository = ...
) -> ListOfArticlesInResponse: ...


async def mark_article_as_favorite(
    article: Article = ...,
    user: User = ...,
    articles_repo: ArticlesRepository = ...
) -> ArticleInResponse: ...


async def remove_article_from_favorites(
    article: Article = ...,
    user: User = ...,
    articles_repo: ArticlesRepository = ...
) -> ArticleInResponse: ...
