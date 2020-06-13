from pypika.queries import Query
from typing import Optional


class Parameter:
    def __init__(self, count: int) -> None: ...


class TypedTable:
    def __init__(
        self,
        name: Optional[str] = ...,
        schema: Optional[str] = ...,
        alias: Optional[str] = ...,
        query_cls: Optional[Query] = ...
    ) -> None: ...
