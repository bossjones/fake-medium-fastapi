from app.db.repositories.tags import TagsRepository
from app.models.schemas.tags import TagsInList


async def get_all_tags(tags_repo: TagsRepository = ...) -> TagsInList: ...
