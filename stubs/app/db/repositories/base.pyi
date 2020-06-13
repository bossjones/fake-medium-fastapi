from asyncpg.connection import Connection


class BaseRepository:
    def __init__(self, conn: Connection) -> None: ...
    @property
    def connection(self) -> Connection: ...
