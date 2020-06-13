from fastapi.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse


async def http_error_handler(
    _: Request,
    exc: HTTPException
) -> JSONResponse: ...
