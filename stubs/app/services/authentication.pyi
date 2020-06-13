from app.db.repositories.users import UsersRepository


async def check_email_is_taken(repo: UsersRepository, email: str) -> bool: ...


async def check_username_is_taken(repo: UsersRepository, username: str) -> bool: ...
