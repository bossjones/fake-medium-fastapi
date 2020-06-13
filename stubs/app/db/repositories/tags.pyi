from typing import (
    List,
    Sequence,
)


class TagsRepository:
    async def create_tags_that_dont_exist(self, *, tags: Sequence[str]) -> None: ...
    async def get_all_tags(self) -> List[str]: ...
