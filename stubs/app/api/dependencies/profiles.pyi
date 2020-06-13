from app.db.repositories.profiles import ProfilesRepository
from app.models.domain.profiles import Profile
from app.models.domain.users import User
from typing import Optional


async def get_profile_by_username_from_path(
    username: str = ...,
    user: Optional[User] = ...,
    profiles_repo: ProfilesRepository = ...
) -> Profile: ...
