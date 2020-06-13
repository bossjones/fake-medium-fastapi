from fastapi.exceptions import RequestValidationError
from pydantic.error_wrappers import ValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse
from typing import Union


async def http422_error_handler(
    _: Request,
    exc: Union[RequestValidationError, ValidationError]
) -> JSONResponse: ...
