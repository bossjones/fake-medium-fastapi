"""
docker tasks
"""
import logging
from invoke import task
from tasks.utils import get_compose_env, is_venv
import click

# from tasks.core import clean, execute_sql

logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")


# click.secho('Hello World!', fg='green')
# click.secho('Some more text', bg='blue', fg='white')
# click.secho('ATTENTION', blink=True, bold=True)
