from fastapi.applications import FastAPI


async def close_db_connection(app: FastAPI) -> None: ...


async def connect_to_db(app: FastAPI) -> None: ...
