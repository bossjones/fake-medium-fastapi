# pylint: disable=E0611
# NOTE: fixes [pylint] No name 'BaseModel' in module 'pydantic'
# SOURCE: https://github.com/nokia-wroclaw/innovativeproject-sudoku/issues/39

from pydantic import BaseModel

from app.models.domain.profiles import Profile


class ProfileInResponse(BaseModel):
    profile: Profile
