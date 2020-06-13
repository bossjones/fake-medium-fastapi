# pylint: disable=E0611
# NOTE: fixes [pylint] No name 'BaseModel' in module 'pydantic'
# SOURCE: https://github.com/nokia-wroclaw/innovativeproject-sudoku/issues/39

from typing import List

from pydantic import BaseModel


class TagsInList(BaseModel):
    tags: List[str]
