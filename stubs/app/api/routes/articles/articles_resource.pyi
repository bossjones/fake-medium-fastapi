from app.db.repositories.articles import ArticlesRepository
from app.models.domain.articles import Article
from app.models.domain.users import User
from app.models.schemas.articles import (
    ArticleInCreate,
    ArticleInResponse,
    ArticleInUpdate,
    ArticlesFilters,
    ListOfArticlesInResponse,
)
from typing import Optional


async def create_new_article(
    article_create: ArticleInCreate = ...,
    user: User = ...,
    articles_repo: ArticlesRepository = ...
) -> ArticleInResponse: ...


async def delete_article_by_slug(
    article: Article = ...,
    articles_repo: ArticlesRepository = ...
) -> None: ...


async def list_articles(
    articles_filters: ArticlesFilters = ...,
    user: Optional[User] = ...,
    articles_repo: ArticlesRepository = ...
) -> ListOfArticlesInResponse: ...


async def retrieve_article_by_slug(
    article: Article = ...
) -> ArticleInResponse: ...


async def update_article_by_slug(
    article_update: ArticleInUpdate = ...,
    current_article: Article = ...,
    articles_repo: ArticlesRepository = ...
) -> ArticleInResponse: ...
