from fastapi.applications import FastAPI
from typing import Callable


def create_start_app_handler(app: FastAPI) -> Callable: ...


def create_stop_app_handler(app: FastAPI) -> Callable: ...
