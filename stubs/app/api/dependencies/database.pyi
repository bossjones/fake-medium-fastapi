from app.db.repositories.base import BaseRepository
from typing import (
    Callable,
    Type,
)


def get_repository(repo_type: Type[BaseRepository]) -> Callable: ...
