from app.db.repositories.profiles import ProfilesRepository
from app.models.domain.profiles import Profile
from app.models.domain.users import User
from app.models.schemas.profiles import ProfileInResponse


async def follow_for_user(
    profile: Profile = ...,
    user: User = ...,
    profiles_repo: ProfilesRepository = ...
) -> ProfileInResponse: ...


async def retrieve_profile_by_username(
    profile: Profile = ...
) -> ProfileInResponse: ...


async def unsubscribe_from_user(
    profile: Profile = ...,
    user: User = ...,
    profiles_repo: ProfilesRepository = ...
) -> ProfileInResponse: ...
