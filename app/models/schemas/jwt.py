# pylint: disable=E0611
# NOTE: fixes [pylint] No name 'BaseModel' in module 'pydantic'
# SOURCE: https://github.com/nokia-wroclaw/innovativeproject-sudoku/issues/39

from datetime import datetime

from pydantic import BaseModel


class JWTMeta(BaseModel):
    exp: datetime
    sub: str


class JWTUser(BaseModel):
    username: str
