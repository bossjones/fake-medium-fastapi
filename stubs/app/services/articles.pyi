from app.db.repositories.articles import ArticlesRepository


async def check_article_exists(articles_repo: ArticlesRepository, slug: str) -> bool: ...


def get_slug_for_article(title: str) -> str: ...
