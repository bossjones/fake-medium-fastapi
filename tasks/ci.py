"""
ci tasks
"""
import logging
from invoke import task, call
import click
from tasks.utils import get_compose_env

# from tasks.core import clean, execute_sql

from .utils import (
    COLOR_WARNING,
    COLOR_DANGER,
    COLOR_SUCCESS,
    COLOR_CAUTION,
    COLOR_STABLE,
)

logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")


@task(incrementable=["verbose"])
def clean(ctx, loc="local", verbose=0, cleanup=False):
    """
    clean compiled python artifacts
    Usage: inv ci.clean
    """
    env = get_compose_env(ctx, loc=loc)

    # Override run commands' env variables one key at a time
    for k, v in env.items():
        ctx.config["run"]["env"][k] = v

    _cmd = r"""
find . -name '*.pyc' -exec rm -fv {} +
find . -name '*.pyo' -exec rm -fv {} +
find . -name '__pycache__' -exec rm -frv {} +
rm -f .coverage
    """

    if verbose >= 1:
        msg = "{}".format(_cmd)
        click.secho(msg, fg=COLOR_SUCCESS)

    ctx.run(_cmd)


@task(incrementable=["verbose"])
def coverage_clean(ctx, loc="local", verbose=0, cleanup=False):
    """
    clean coverage files
    Usage: inv ci.coverage-clean
    """
    env = get_compose_env(ctx, loc=loc)

    # Override run commands' env variables one key at a time
    for k, v in env.items():
        ctx.config["run"]["env"][k] = v

    _cmd = r"""
find . -name '*.pyc' -exec rm -fv {} +
find . -name '*.pyo' -exec rm -fv {} +
find . -name '__pycache__' -exec rm -frv {} +
rm -f .coverage
rm -rf htmlcov/*
rm -rf cov_annotate/*
rm -f cov.xml
    """

    if verbose >= 1:
        msg = "{}".format(_cmd)
        click.secho(msg, fg=COLOR_SUCCESS)

    ctx.run(_cmd)


@task
def pylint(ctx, loc="local", tests=False, everything=False, specific=""):
    """
    pylint fake-medium-fastapi folder
    Usage: inv ci.pylint
    """
    env = get_compose_env(ctx, loc=loc)

    # Only display result
    ctx.config["run"]["echo"] = True

    # Override run commands env variables one key at a time
    for k, v in env.items():
        ctx.config["run"]["env"][k] = v

    if tests:
        ctx.run(
            "poetry run pylint --disable=all --enable=F,E --rcfile ./lint-configs-python/python/pylintrc tests"
        )
    elif everything:
        ctx.run(
            "poetry run pylint --rcfile ./lint-configs-python/python/pylintrc tests app"
        )
    elif specific:
        ctx.run(
            f"poetry run pylint --disable=all --enable={specific} --rcfile ./lint-configs-python/python/pylintrc tests app"
        )
    else:
        ctx.run(
            "poetry run pylint --disable=all --enable=F,E --rcfile ./lint-configs-python/python/pylintrc app"
        )


@task(incrementable=["verbose"])
def mypy(ctx, loc="local", verbose=0):
    """
    mypy fake-medium-fastapi folder
    Usage: inv ci.mypy
    """
    env = get_compose_env(ctx, loc=loc)

    # Only display result
    ctx.config["run"]["echo"] = True

    # Override run commands env variables one key at a time
    for k, v in env.items():
        ctx.config["run"]["env"][k] = v

    # ctx.run("poetry run mypy --config-file ./lint-configs-python/python/mypy.ini app tests")
    ctx.run("poetry run mypy --config-file ./setup.cfg app tests")


@task(
    pre=[call(clean, loc="local"),], incrementable=["verbose"],
)
def black(ctx, loc="local", check=False, debug=False, verbose=0, tests=False):
    """
    Run black code formatter
    Usage: inv ci.black
    """
    env = get_compose_env(ctx, loc=loc)

    # Only display result
    ctx.config["run"]["echo"] = True

    # Override run commands env variables one key at a time
    for k, v in env.items():
        ctx.config["run"]["env"][k] = v

    _cmd = "poetry run black "

    if check:
        _cmd += "--check "

    if verbose >= 3:
        _cmd += "--verbose "

    if tests:
        _cmd += "tests tasks "

    _cmd += "app"

    if verbose >= 1:
        msg = "[black] bout to run command: \n"
        click.secho(msg, fg="green")
        click.secho(_cmd, fg="green")

    ctx.run(_cmd)


@task(
    pre=[call(clean, loc="local"),], incrementable=["verbose"],
)
def isort(
    ctx, loc="local", check=False, dry_run=False, verbose=0, apply=False, diff=False
):
    """
    isort fake-medium-fastapi module. Some of the arguments were taken from the starlette contrib scripts. Tries to align w/ black to prevent having to reformat multiple times.

    To check mode only(does not make changes permenantly):
        Usage: inv ci.isort --check -vvv
    Simply display command we would run:
        Usage: inv ci.isort --check --dry-run -vvv
    """
    env = get_compose_env(ctx, loc=loc)

    # Only display result
    ctx.config["run"]["echo"] = True

    # Override run commands env variables one key at a time
    for k, v in env.items():
        ctx.config["run"]["env"][k] = v

    _cmd = "poetry run isort --recursive"

    if check:
        _cmd += " --check-only"

    if diff:
        _cmd += " --diff"

    if verbose >= 2:
        _cmd += " --verbose"

    if apply:
        _cmd += " --apply"

    _cmd += " app tests"

    if verbose >= 1:
        msg = "{}".format(_cmd)
        click.secho(msg, fg=COLOR_SUCCESS)

    if dry_run:
        click.secho(
            "[isort] DRY RUN mode enabled, not executing command: {}".format(_cmd),
            fg=COLOR_CAUTION,
        )
    else:
        ctx.run(_cmd)


@task
def verify_python_version(ctx, loc="local", check=True, debug=False):
    """
    verify_python_version is 3.8.2
    """
    env = get_compose_env(ctx, loc=loc)

    # Only display result
    ctx.config["run"]["echo"] = True

    # Override run commands env variables one key at a time
    for k, v in env.items():
        ctx.config["run"]["env"][k] = v

    # Python 3.8.2
    res = ctx.run("python --version")

    assert "Python 3.8.2" in res.stdout.rstrip()


@task
def pre_start(ctx, loc="local", check=True, debug=False):
    """
    pre_start fake-medium-fastapi module
    """
    env = get_compose_env(ctx, loc=loc)

    # Only display result
    ctx.config["run"]["echo"] = True

    # Override run commands env variables one key at a time
    for k, v in env.items():
        ctx.config["run"]["env"][k] = v

    # ctx.run("python app/api/tests_pre_start.py")


@task(incrementable=["verbose"])
def pytest(
    ctx,
    loc="local",
    check=True,
    debug=False,
    verbose=0,
    pdb=False,
    # configonly=False,
    # settingsonly=False,
    # pathsonly=False,
    # workspaceonly=False,
    # clientonly=False,
    # fastapionly=False,
    # jwtonly=False,
    # mockedfs=False,
    # clionly=False,
    # usersonly=False,
    # convertingtotestclientstarlette=False,
    # loggeronly=False,
    # utilsonly=False,
):
    """
    Run pytest
    Usage: inv ci.pytest
    """
    env = get_compose_env(ctx, loc=loc)

    # Only display result
    ctx.config["run"]["echo"] = True

    # Override run commands env variables one key at a time
    for k, v in env.items():
        ctx.config["run"]["env"][k] = v

    _cmd = r"poetry run py.test"

    if verbose >= 1:
        msg = "[pytest] check mode disabled"
        click.secho(msg, fg="green")
        _cmd += r" --verbose "

    # if configonly:
    #     _cmd += r" -m configonly "

    # if pathsonly:
    #     _cmd += r" -m pathsonly "

    # if settingsonly:
    #     _cmd += r" -m settingsonly "

    # if workspaceonly:
    #     _cmd += r" -m workspaceonly "

    # if clientonly:
    #     _cmd += r" -m clientonly "

    # if fastapionly:
    #     _cmd += r" -m fastapionly "

    # if jwtonly:
    #     _cmd += r" -m jwtonly "

    # if mockedfs:
    #     _cmd += r" -m mockedfs "

    # if clionly:
    #     _cmd += r" -m clionly "

    # if usersonly:
    #     _cmd += r" -m usersonly "

    # if convertingtotestclientstarlette:
    #     _cmd += r" -m convertingtotestclientstarlette "

    # if loggeronly:
    #     _cmd += r" -m loggeronly "

    # if utilsonly:
    #     _cmd += r" -m utilsonly "

    if pdb:
        _cmd += r" --pdb "

    _cmd += r" --cov-config=setup.cfg --verbose --cov-append --cov-report=term-missing --cov-report=xml:cov.xml --cov-report=html:htmlcov --cov-report=annotate:cov_annotate --mypy --showlocals --tb=short --cov=app tests"

    ctx.run(_cmd)


@task(incrementable=["verbose"])
def view_coverage(ctx, loc="local"):
    """
    Open coverage report inside of browser
    Usage: inv ci.view-coverage
    """
    env = get_compose_env(ctx, loc=loc)

    # Only display result
    ctx.config["run"]["echo"] = True

    # Override run commands env variables one key at a time
    for k, v in env.items():
        ctx.config["run"]["env"][k] = v

    _cmd = r"./script/open-browser.py file://${PWD}/htmlcov/index.html"

    ctx.run(_cmd)


@task(
    incrementable=["verbose"],
    aliases=["swagger", "openapi", "view_openapi", "view_swagger"],
)
def view_api_docs(ctx, loc="local"):
    """
    Open api swagger docs inside of browser
    Usage: inv ci.view-api-docs
    """
    env = get_compose_env(ctx, loc=loc)

    # Only display result
    ctx.config["run"]["echo"] = True

    # Override run commands env variables one key at a time
    for k, v in env.items():
        ctx.config["run"]["env"][k] = v

    _cmd = r"./script/open-browser.py http://localhost:8000/docs"

    ctx.run(_cmd)


@task(
    incrementable=["verbose"],
    pre=[call(view_api_docs, loc="local"), call(view_coverage, loc="local"),],
)
def browser(ctx, loc="local"):
    """
    Open api swagger docs inside of browser
    Usage: inv ci.view-api-docs
    """
    env = get_compose_env(ctx, loc=loc)

    # Only display result
    ctx.config["run"]["echo"] = True

    # Override run commands env variables one key at a time
    for k, v in env.items():
        ctx.config["run"]["env"][k] = v

    msg = "Finished loading everything into browser"
    click.secho(msg, fg=COLOR_SUCCESS)


@task(incrementable=["verbose"])
def alembic_upgrade(ctx, loc="local"):
    """
    Run alembic upgrade head
    Usage: inv ci.alembic-upgrade
    """
    env = get_compose_env(ctx, loc=loc)

    # Only display result
    ctx.config["run"]["echo"] = True

    # Override run commands env variables one key at a time
    for k, v in env.items():
        ctx.config["run"]["env"][k] = v

    _cmd = r"poetry run alembic upgrade head"

    ctx.run(_cmd)


@task(incrementable=["verbose"])
def editable(ctx, loc="local"):
    """
    Run: pip install -e .
    Usage: inv ci.editable
    """
    env = get_compose_env(ctx, loc=loc)

    # Only display result
    ctx.config["run"]["echo"] = True

    # Override run commands env variables one key at a time
    for k, v in env.items():
        ctx.config["run"]["env"][k] = v

    _cmd = r"poetry install"

    ctx.run(_cmd)


@task(
    pre=[
        call(clean, loc="local"),
        call(verify_python_version, loc="local"),
        call(pre_start, loc="local"),
        call(alembic_upgrade, loc="local"),
    ],
    incrementable=["verbose"],
)
def monkeytype(
    ctx,
    loc="local",
    verbose=0,
    cleanup=False,
    test=False,
    apply=False,
    stub=False,
    dry_run=False,
):
    """
    Use monkeytype to collect runtime types of function arguments and return values, and automatically generate stub files
    or even add draft type annotations directly to python code. Uses pytest to access all lines of code that have testing setup.

    To generate stubs:
        Usage: inv ci.monkeytype --test -vvv
    To apply stubs to existing code base:
        Usage: inv ci.monkeytype --test --apply --stub -vvv
    To apply stubs to existing code base(dry run):
        Usage: inv ci.monkeytype --test --apply --stub -vvv --dry-run
    """
    env = get_compose_env(ctx, loc=loc)

    # Only display result
    ctx.config["run"]["echo"] = True

    # Override run commands' env variables one key at a time
    for k, v in env.items():
        ctx.config["run"]["env"][k] = v

    # NOTE: https://monkeytype.readthedocs.io/en/stable/faq.html#why-did-my-test-coverage-measurement-stop-working
    _cmd = r"""poetry run monkeytype run "`command -v pytest`" --no-cov --verbose --mypy --showlocals --tb=short tests"""

    if test:
        if verbose >= 1:
            msg = "{}".format(_cmd)
            click.secho(msg, fg=COLOR_SUCCESS)

        if dry_run:
            click.secho(
                "[monkeytype] DRY RUN mode enabled, not executing command: {}".format(
                    _cmd
                ),
                fg=COLOR_CAUTION,
            )
        else:
            ctx.run(_cmd)

    _cmd_stub = r"""
modules_array=()
while IFS= read -r line; do
    modules_array+=( "$line" )
done < <( monkeytype list-modules | grep -v "pytestipdb" | grep -v "fdf8821871d7_main_tables" | grep -v "env_py" )

echo "Stub all modules using monkeytype"
for element in "${modules_array[@]}"
do
    filename=$(echo $element | sed 's,\.,\/,g')
    _basedir=$(dirname "$filename")
    mkdir -p stubs/$_basedir || true
    touch stubs/$_basedir/__init__.pyi
    echo " [run] monkeytype stub ${element} > stubs/$filename.pyi"
    monkeytype -v stub ${element} > stubs/$filename.pyi
done

    """

    if stub:
        if dry_run:
            click.secho(
                "[monkeytype] DRY RUN mode enabled, not executing command: \n\n{}".format(
                    _cmd_stub
                ),
                fg=COLOR_CAUTION,
            )
        else:
            ctx.run(_cmd_stub)

    _cmd_apply = r"""
modules_array=()
while IFS= read -r line; do
    modules_array+=( "$line" )
done < <( monkeytype list-modules | grep -v "pytestipdb" | grep -v "fdf8821871d7_main_tables" | grep -v "env_py" )

echo "apply all modules using monkeytype"
for element in "${modules_array[@]}"
do
    monkeytype apply ${element}
done
    """
    #     _cmd_apply = r"""
    # find stubs -type f -name '*.pyi' ! -name '*.venv' -print0 | xargs -I FILE -t -0 -n1 monkeytype -v apply FILE
    #     """

    # find stubs -type f -name '*.pyi' ! -name '*.venv' -print0 | xargs -I FILE -t -0 -n1 monkeytype -v apply FILE

    if apply:
        if dry_run:
            click.secho(
                "[monkeytype] DRY RUN mode enabled, not executing command: \n\n{}".format(
                    _cmd_apply
                ),
                fg=COLOR_CAUTION,
            )
        else:
            ctx.run(_cmd_apply)


@task(incrementable=["verbose"])
def autoflake(
    ctx,
    loc="local",
    verbose=0,
    check=False,
    dry_run=False,
    in_place=False,
    remove_all_unused_imports=False,
):
    """
    Use autoflake to remove unused imports, recursively, remove unused variables, and exclude __init__.py

    To run autoflake in check only mode:
        Usage: inv ci.autoflake --check -vvv
    To run autoflake in check only mode(dry-run):
        Usage: inv ci.autoflake --check -vvv --dry-run
    To run autoflake inplace w/(dry-run):
        Usage: inv ci.autoflake --in-place -vvv --dry-run
    """
    env = get_compose_env(ctx, loc=loc)

    # Only display result
    ctx.config["run"]["echo"] = True

    # Override run commands' env variables one key at a time
    for k, v in env.items():
        ctx.config["run"]["env"][k] = v

    # To remove all unused imports (whether or not they are from the standard library), use the --remove-all-unused-imports option.
    _cmd = "poetry run autoflake"
    _cmd += " --recursive --remove-unused-variables"

    if remove_all_unused_imports:
        _cmd += " --remove-all-unused-imports "

    if check:
        _cmd += " --check"

    if in_place:
        _cmd += " --in-place"

    _cmd += " --exclude=__init__.py"
    _cmd += " app"
    _cmd += " tests"
    _cmd += " tasks"

    if verbose >= 1:
        msg = "{}".format(_cmd)
        click.secho(msg, fg=COLOR_SUCCESS)

    if dry_run:
        click.secho(
            "[autoflake] DRY RUN mode enabled, not executing command: {}".format(_cmd),
            fg=COLOR_CAUTION,
        )
    else:
        ctx.run(_cmd)


@task(
    pre=[call(clean, loc="local"), call(verify_python_version, loc="local"),],
    incrementable=["verbose"],
    aliases=["clean_stubs", "clean_monkeytype"],
)
def clean_pyi(ctx, loc="local", verbose=0, dry_run=False):
    """
    Clean all stub files

    To clean stubs:
        Usage: inv ci.clean-pyi -vvv
    To clean stubs(dry run):
        Usage: inv ci.clean-pyi -vvv --dry-run
    """
    env = get_compose_env(ctx, loc=loc)

    # Only display result
    ctx.config["run"]["echo"] = True

    # Override run commands' env variables one key at a time
    for k, v in env.items():
        ctx.config["run"]["env"][k] = v

    # NOTE: https://monkeytype.readthedocs.io/en/stable/faq.html#why-did-my-test-coverage-measurement-stop-working
    _cmd = r"""find . -name '*.pyi' -exec rm -fv {} +"""

    if verbose >= 1:
        msg = "{}".format(_cmd)
        click.secho(msg, fg=COLOR_SUCCESS)

    if dry_run:
        click.secho(
            "[monkeytype] DRY RUN mode enabled, not executing command: {}".format(_cmd),
            fg=COLOR_CAUTION,
        )
    else:
        ctx.run(_cmd)


@task(
    pre=[
        call(clean, loc="local"),
        call(verify_python_version, loc="local"),
        # call(pre_start, loc="local"),
        call(alembic_upgrade, loc="local"),
        # call(pytest, loc="local", configonly=True),
        # call(pytest, loc="local", settingsonly=True),
        # call(pytest, loc="local", pathsonly=True),
        # call(pytest, loc="local", workspaceonly=True),
        # call(pytest, loc="local", clientonly=True),
        # call(pytest, loc="local", fastapionly=True),
        # call(pytest, loc="local", utilsonly=True),
        # call(pytest, loc="local", jwtonly=True),
        # call(pytest, loc="local", mockedfs=True),
        # call(pytest, loc="local", clionly=True),
        # call(pytest, loc="local", usersonly=True),
        # call(pytest, loc="local", convertingtotestclientstarlette=True),
        # call(pytest, loc="local", loggeronly=True),
        call(pytest, loc="local"),
    ],
    incrementable=["verbose"],
)
def travis(ctx, loc="local", check=True, debug=False, verbose=0):
    """
    Run travis
    Usage: inv ci.travis
    """
    env = get_compose_env(ctx, loc=loc)

    # Only display result
    ctx.config["run"]["echo"] = True

    # Override run commands env variables one key at a time
    for k, v in env.items():
        ctx.config["run"]["env"][k] = v

    if verbose >= 1:
        msg = "[travis] check mode disabled"
        click.secho(msg, fg="green")
    #     _cmd = r"""
    # mv -f .coverage .coverage.tests || true
    # coverage combine
    # """
    _cmd = r"""
pytest
"""

    ctx.run(_cmd)


@task(
    pre=[
        call(clean, loc="local"),
        call(verify_python_version, loc="local"),
        call(pre_start, loc="local"),
        call(alembic_upgrade, loc="local"),
        call(mypy, loc="local"),
        call(autoflake, loc="local", in_place=True),
        call(black, loc="local", check=False),
        call(isort, loc="local", apply=True),
        call(black, loc="local", check=False),
        call(mypy, loc="local"),
        call(pytest, loc="local"),
    ],
    incrementable=["verbose"],
)
def lint(ctx, loc="local", check=True, debug=False, verbose=0):
    """
    Run all static analysis[mypy,autoflake,black,isort,black,mypy,pytest]
    Usage: inv ci.lint
    """
    env = get_compose_env(ctx, loc=loc)

    # Only display result
    ctx.config["run"]["echo"] = True

    # Override run commands env variables one key at a time
    for k, v in env.items():
        ctx.config["run"]["env"][k] = v

    if verbose >= 1:
        msg = "[lint] check mode disabled"
        click.secho(msg, fg="green")


@task(
    pre=[call(clean, loc="local"),], incrementable=["verbose"],
)
def postman(
    ctx, loc="local", dry_run=False, verbose=0
):
    """
    Run integration tests against active api server.
    """
    env = get_compose_env(ctx, loc=loc)

    # Only display result
    ctx.config["run"]["echo"] = True

    # Override run commands env variables one key at a time
    for k, v in env.items():
        ctx.config["run"]["env"][k] = v

    _cmd = "poetry run ./postman/run-api-tests.sh"

    if verbose >= 1:
        msg = "{}".format(_cmd)
        click.secho(msg, fg=COLOR_SUCCESS)

    if dry_run:
        click.secho(
            "[postman] DRY RUN mode enabled, not executing command: {}".format(_cmd),
            fg=COLOR_CAUTION,
        )
    else:
        ctx.run(_cmd)
