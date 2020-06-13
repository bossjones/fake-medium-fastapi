IMPORTANT
----------
I just wanted to try messing around with an already "complete" project that uses fastapi. This is pretty much a clone of the work that https://github.com/nsidnev/fastapi-realworld-example-app has done, and I only indend to use this for learning purposes.

|

.. image:: https://github.com/bossjones/fake-medium-fastapi/workflows/API%20spec/badge.svg
   :target: https://github.com/bossjones/fake-medium-fastapi

.. image:: https://github.com/bossjones/fake-medium-fastapi/workflows/Tests/badge.svg
   :target: https://github.com/bossjones/fake-medium-fastapi

.. image:: https://github.com/bossjones/fake-medium-fastapi/workflows/Styles/badge.svg
   :target: https://github.com/bossjones/fake-medium-fastapi

.. image:: https://github.com/bossjones/fake-medium-fastapi/workflows/Deploy/badge.svg
   :target: https://frw.nsidnev.dev/

.. image:: https://codecov.io/gh/nsidnev/fake-medium-fastapi/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/nsidnev/fake-medium-fastapi

.. image:: https://img.shields.io/github/license/Naereen/StrapDown.js.svg
   :target: https://github.com/bossjones/fake-medium-fastapi/blob/master/LICENSE

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/ambv/black

.. image:: https://img.shields.io/badge/style-wemake-000000.svg
   :target: https://github.com/wemake-services/wemake-python-styleguide

Quickstart
----------

First, run ``PostgreSQL``, set environment variables and create database. For example using ``docker``: ::

    export POSTGRES_DB=rwdb POSTGRES_PORT=5432 POSTGRES_USER=postgres POSTGRES_PASSWORD=postgres
    docker run --name pgdb --rm -e POSTGRES_USER="$POSTGRES_USER" -e POSTGRES_PASSWORD="$POSTGRES_PASSWORD" -e POSTGRES_DB="$POSTGRES_DB" postgres
    export POSTGRES_HOST=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' pgdb)
    createdb --host=$POSTGRES_HOST --port=$POSTGRES_PORT --username=$POSTGRES_USER $POSTGRES_DB

Then run the following commands to bootstrap your environment with ``poetry``: ::

    git clone https://github.com/bossjones/fake-medium-fastapi
    cd fake-medium-fastapi
    poetry install
    poetry shell

Then create ``.env`` file (or rename and modify ``.env.example``) in project root and set environment variables for application: ::

    touch .env
    echo DB_CONNECTION=postgresql://$POSTGRES_USER:$POSTGRES_PASSWORD@$POSTGRES_HOST:$POSTGRES_PORT/$POSTGRES_DB >> .env
    echo SECRET_KEY=$(openssl rand -hex 32) >> .env

To run the web application in debug use::

    alembic upgrade head
    uvicorn app.main:app --reload


Deployment with Docker
----------------------

You must have ``docker`` and ``docker-compose`` tools installed to work with material in this section.
First, create ``.env`` file like in `Quickstart` section or modify ``.env.example``.
``POSTGRES_HOST`` must be specified as `db` or modified in ``docker-compose.yml`` also.
Then just run::

    docker-compose up -d db
    docker-compose up -d app

Application will be available on ``localhost`` in your browser.

Web routes
----------

All routes are available on ``/docs`` or ``/redoc`` paths with Swagger or ReDoc.


Project structure
-----------------

Files related to application are in the ``app`` or ``tests`` directories.
Application parts are:

::

    app
    ├── api              - web related stuff.
    │   ├── dependencies - dependencies for routes definition.
    │   ├── errors       - definition of error handlers.
    │   └── routes       - web routes.
    ├── core             - application configuration, startup events, logging.
    ├── db               - db related stuff.
    │   ├── migrations   - manually written alembic migrations.
    │   └── repositories - all crud stuff.
    ├── models           - pydantic models for this application.
    │   ├── domain       - main models that are used almost everywhere.
    │   └── schemas      - schemas for using in web routes.
    ├── resources        - strings that are used in web responses.
    ├── services         - logic that is not just crud related.
    └── main.py          - FastAPI application creation and configuration.
