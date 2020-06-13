from app.models.domain.users import User
from datetime import timedelta
from typing import Dict


def create_access_token_for_user(user: User, secret_key: str) -> str: ...


def create_jwt_token(*, jwt_content: Dict[str, str], secret_key: str, expires_delta: timedelta) -> str: ...


def get_username_from_token(token: str, secret_key: str) -> str: ...
