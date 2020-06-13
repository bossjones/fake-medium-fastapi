from typing import (
    Callable,
    Type,
)


def do_with_retry(catching_exc: Type[Exception], reraised_exc: Type[Exception], error_msg: str) -> Callable: ...


def ping_postgres(dsn: str) -> None: ...
