"""
travis tasks
"""
import logging
from invoke import task, call
import click
from tasks.utils import get_compose_env

from .git import pr_sha

from .utils import (
    COLOR_WARNING,
    COLOR_DANGER,
    COLOR_SUCCESS,
    COLOR_CAUTION,
    COLOR_STABLE,
)

logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")

CI_IMAGE = "bossjones/fake-medium-fastapi-ci"

# .PHONY: travis
# travis: travis-pull travis-build dc-up-web ci-test ## Bring up web server using docker-compose, then exec into container and run pytest
# # tox


@task(incrementable=["verbose"])
def pull(ctx, loc="docker", image=CI_IMAGE, verbose=0):
    """
    Docker pull base and run-image tags
    Usage: inv travis.pull
    """
    env = get_compose_env(ctx, loc=loc)

    # Override run commands' env variables one key at a time
    for k, v in env.items():
        ctx.config["run"]["env"][k] = v

    # override CI_IMAGE value
    ctx.config["run"]["env"]["CI_IMAGE"] = image

    _cmds = [
        "docker pull {CI_IMAGE}:base || true".format(CI_IMAGE=image),
        "docker pull {CI_IMAGE}:runtime-image || true".format(CI_IMAGE=image),
    ]

    ctx.run(_cmds[0])
    ctx.run(_cmds[1])


@task(incrementable=["verbose"])
def container_uid(ctx, loc="docker", verbose=0):
    """
    Docker container_uid base and run-image tags
    Usage: inv travis.container_uid
    """
    env = get_compose_env(ctx, loc=loc)

    # Override run commands' env variables one key at a time
    for k, v in env.items():
        ctx.config["run"]["env"][k] = v

    res = ctx.run("id -u")

    ctx.config["run"]["env"]["CONTAINER_UID"] = "{}".format(res.stdout)


@task(incrementable=["verbose"])
def container_gid(ctx, loc="docker", verbose=0):
    """
    Docker container_gid base and run-image tags
    Usage: inv travis.container_gid
    """
    env = get_compose_env(ctx, loc=loc)

    # Override run commands' env variables one key at a time
    for k, v in env.items():
        ctx.config["run"]["env"][k] = v

    res = ctx.run("id -g")

    ctx.config["run"]["env"]["CONTAINER_GID"] = "{}".format(res.stdout)


@task(incrementable=["verbose"])
def pip_cache(ctx, loc="docker", verbose=0):
    """
    Configure pip cache env vars
    Usage: inv travis.pip_cache
    """
    env = get_compose_env(ctx, loc=loc)

    # Override run commands' env variables one key at a time
    for k, v in env.items():
        ctx.config["run"]["env"][k] = v

    ctx.config["run"]["env"]["STANDARD_CACHE_DIR"] = "~/.cache/pip"
    ctx.config["run"]["env"]["WHEELHOUSE"] = "{}/wheels".format(
        ctx.config["run"]["env"]["STANDARD_CACHE_DIR"]
    )
    ctx.config["run"]["env"]["PIP_WHEEL_DIR"] = "{}".format(
        ctx.config["run"]["env"]["WHEELHOUSE"]
    )

    # ctx.config["run"]["env"]["CONTAINER_GID"] = "{}".format(res.stdout)
    # SOURCE: https://blog.ionelmc.ro/2015/01/02/speedup-pip-install/
    # export STANDARD_CACHE_DIR="${XDG_CACHE_HOME:-${HOME}/.cache}/pip"
    # export WHEELHOUSE="${STANDARD_CACHE_DIR}/wheels"
    # export PIP_FIND_LINKS="file://${WHEELHOUSE}"
    # export PIP_WHEEL_DIR="${WHEELHOUSE}"


@task(incrementable=["verbose"])
def env_set(ctx, loc="docker", image=CI_IMAGE, verbose=0):
    """
    Configure env for travis builds
    Usage: inv travis.env-set
    """
    env = get_compose_env(ctx, loc=loc)

    # Override run commands' env variables one key at a time
    for k, v in env.items():
        ctx.config["run"]["env"][k] = v

    # override CI_IMAGE value
    ctx.config["run"]["env"]["CI_IMAGE"] = image
    ctx.config["run"]["env"]["CACHE_DIR"] = "$HOME/.cache/docker"
    ctx.config["run"]["env"]["CACHE_FILE_BASE"] = "$CACHE_DIR/base.tar.gz"
    ctx.config["run"]["env"]["CACHE_FILE_RUNTIME"] = "$CACHE_DIR/runtime-image.tar.gz"
    ctx.config["run"]["env"]["IS_CI_ENVIRONMENT"] = "true"


@task(
    pre=[
        call(pr_sha, loc="docker"),
        call(container_uid, loc="docker"),
        call(container_gid, loc="docker"),
        call(pip_cache, loc="docker"),
        call(env_set, loc="docker"),
    ],
    incrementable=["verbose"],
)
def preflight(ctx, loc="docker", image=CI_IMAGE, verbose=0):
    """
    Configure env for travis builds
    Usage: inv travis.env-set
    """
    env = get_compose_env(ctx, loc=loc)

    # Override run commands' env variables one key at a time
    for k, v in env.items():
        ctx.config["run"]["env"][k] = v

    _VALIDATE_ENVS = [
        "CI_IMAGE",
        "CACHE_DIR",
        "CACHE_FILE_BASE",
        "CACHE_FILE_RUNTIME",
        "IS_CI_ENVIRONMENT",
        "CONTAINER_UID",
        "CONTAINER_GID",
        "TAG",
        "STANDARD_CACHE_DIR",
        "WHEELHOUSE",
        "PIP_WHEEL_DIR",
    ]

    # Verify everything has been set that we care about.
    # TODO: Move this into its own private task, so it can be called from anywhere
    for v in _VALIDATE_ENVS:
        assert ctx.config["run"]["env"][v]
        if verbose >= 1:
            msg = "[preflight] {}={}".format(v, ctx.config["run"]["env"][v])
            click.secho(msg, fg=COLOR_SUCCESS)


# .PHONY: ci-build
# ci-build: ci-before_install dc-build-cache-base dc-up-web ci-gunzip # build docker cache base, cache it locally on machine and send up to docker hub etc


@task(
    pre=[call(preflight, loc="docker"),], incrementable=["verbose"],
)
def build_gunzip_before_install(ctx, loc="docker", image=CI_IMAGE, verbose=0):
    """
    docker container/image from gnzip tar file in $HOME/.cache/docker
    Usage: inv travis.build_gunzip_before_install
    """
    env = get_compose_env(ctx, loc=loc)

    # Override run commands' env variables one key at a time
    for k, v in env.items():
        ctx.config["run"]["env"][k] = v

    if verbose >= 1:
        msg = "[build-gunzip-before-install] Building using docker-compose"
        click.secho(msg, fg=COLOR_SUCCESS)

    _cmd = r"""
if [ -f ${CACHE_FILE_BASE} ]; then gunzip -c ${CACHE_FILE_BASE} | docker load || true; fi
if [ -f ${CACHE_FILE_RUNTIME} ]; then gunzip -c ${CACHE_FILE_RUNTIME} | docker load || true; fi
    """

    if verbose >= 1:
        msg = "[build-gunzip-before-install] cmd is: "
        click.secho(msg, fg=COLOR_SUCCESS)

        msg = "{}".format(_cmd)
        click.secho(msg, fg=COLOR_SUCCESS)

    ctx.run(_cmd)


@task(
    pre=[call(build_gunzip_before_install, loc="docker"),], incrementable=["verbose"],
)
def dc_build_cache_base(ctx, loc="docker", image=CI_IMAGE, verbose=0):
    """
    docker pull intermediate docker cache and build what we are missing, finally push it up to docker hub so we have a cache ready to go.
    Usage: inv travis.dc-build-cache-base
    """
    env = get_compose_env(ctx, loc=loc)

    # Override run commands' env variables one key at a time
    for k, v in env.items():
        ctx.config["run"]["env"][k] = v

    # TODO: Split this into subtask
    click.secho(
        "[dc-build-cache-base] pull docker cache from docker hub if available",
        fg=COLOR_SUCCESS,
    )
    ctx.run("time docker pull $REPO_NAME:base || true")
    ctx.run("time docker pull $REPO_NAME:runtime-image || true")

    # TODO: Split this into subtask
    click.secho("[dc-build-cache-base] docker-compose build 'base'", fg=COLOR_SUCCESS)
    ctx.run("time docker-compose -f docker-compose.base.yml build")

    # TODO: Split this into subtask
    click.secho(
        "[dc-build-cache-base] docker-compose push '$REPO_NAME:base'", fg=COLOR_SUCCESS
    )
    ctx.run("time docker push $REPO_NAME:base || true")

    # TODO: Split this into subtask
    click.secho(
        "[dc-build-cache-base] docker-compose pull '$REPO_NAME:runtime-image'",
        fg=COLOR_SUCCESS,
    )
    ctx.run("time docker pull $REPO_NAME:runtime-image || true")

    # TODO: Split this into subtask
    click.secho(
        "[dc-build-cache-base] docker-compose build '$REPO_NAME:runtime-image'",
        fg=COLOR_SUCCESS,
    )
    ctx.run("time docker-compose -f docker-compose.ci.yml build")

    # TODO: Split this into subtask
    click.secho(
        "[dc-build-cache-base] docker-compose push '$REPO_NAME:runtime-image'",
        fg=COLOR_SUCCESS,
    )
    ctx.run("time docker push $REPO_NAME:runtime-image || true")


@task(
    pre=[call(dc_build_cache_base, loc="docker"),], incrementable=["verbose"],
)
def dc_up_web(ctx, loc="docker", image=CI_IMAGE, verbose=0):
    """
    start up fastapi server via docker-compose, daemonized
    Usage: inv travis.dc-up-web
    """
    env = get_compose_env(ctx, loc=loc)

    # Override run commands' env variables one key at a time
    for k, v in env.items():
        ctx.config["run"]["env"][k] = v

    if ctx.config["run"]["env"]["IS_CI_ENVIRONMENT"] == "true":

        if verbose >= 1:
            msg = "[dc-up-web] IS_CI_ENVIRONMENT env var detected. Overriding CONTAINER_UID and CONTAINER_GID"
            click.secho(msg, fg=COLOR_SUCCESS)

        res_travis_uid = ctx.run("ls -lta | awk '{print $3}'")
        res_travis_gid = ctx.run("ls -lta | awk '{print $4}'")

        ctx.config["run"]["env"]["CONTAINER_UID"] = "{}".format(res_travis_uid.stdout)
        ctx.config["run"]["env"]["CONTAINER_GID"] = "{}".format(res_travis_gid.stdout)

        if verbose >= 1:
            click.secho(
                "[dc-up-web] CONTAINER_UID={}".format(
                    ctx.config["run"]["env"]["CONTAINER_UID"], fg=COLOR_SUCCESS
                )
            )
            click.secho(
                "[dc-up-web] CONTAINER_GID={}".format(
                    ctx.config["run"]["env"]["CONTAINER_GID"], fg=COLOR_SUCCESS
                )
            )

    click.secho(
        " [dc_up_web] Remove possibly previous broken stacks left hanging after an error",
        fg=COLOR_SUCCESS,
    )
    ctx.run("docker-compose -f docker-compose.ci.yml down -v --remove-orphans")

    click.secho(" [dc_up_web] docker-compose up daemonized", fg=COLOR_SUCCESS)
    ctx.run("docker-compose -f docker-compose.ci.yml -f docker-compose.web.yml up -d")


@task(
    pre=[call(dc_up_web, loc="docker"),], incrementable=["verbose"],
)
def gunzip_save(ctx, loc="docker", image=CI_IMAGE, verbose=0):
    """
    take contents of dockerfile and cache it locally into $HOME/.cache/docker
    Usage: inv travis.gunzip-save
    """
    env = get_compose_env(ctx, loc=loc)

    # Override run commands' env variables one key at a time
    for k, v in env.items():
        ctx.config["run"]["env"][k] = v

    if verbose >= 1:
        click.secho(" [gunzip-save] travis 'install:' section", fg=COLOR_SUCCESS)
        click.secho(
            " [gunzip-save] pull docker cache from docker hub if available",
            fg=COLOR_SUCCESS,
        )

    _cmd = r"""
mkdir -p $CACHE_DIR
if [ ! -f ${CACHE_FILE_BASE} ]; then docker save $REPO_NAME:base | gzip > ${CACHE_FILE_BASE} || true; fi

if [ ! -f ${CACHE_FILE_RUNTIME} ]; then docker save $REPO_NAME:runtime-image | gzip > ${CACHE_FILE_RUNTIME} || true; fi
    """

    if verbose >= 1:
        msg = "[build-gunzip-before-install] cmd is: "
        click.secho(msg, fg=COLOR_SUCCESS)

        msg = "{}".format(_cmd)
        click.secho(msg, fg=COLOR_SUCCESS)

    ctx.run(_cmd)


@task(
    pre=[call(gunzip_save, loc="docker"),], incrementable=["verbose"],
)
def test(ctx, loc="docker", image=CI_IMAGE, verbose=0):
    """
    take contents of dockerfile and cache it locally into $HOME/.cache/docker
    Usage: inv travis.gunzip-save
    """
    env = get_compose_env(ctx, loc=loc)

    # Override run commands' env variables one key at a time
    for k, v in env.items():
        ctx.config["run"]["env"][k] = v

    if ctx.config["run"]["env"]["IS_CI_ENVIRONMENT"] == "true":

        if verbose >= 1:
            msg = "[test] IS_CI_ENVIRONMENT env var detected. Overriding CONTAINER_UID and CONTAINER_GID"
            click.secho(msg, fg=COLOR_SUCCESS)

        res_travis_uid = ctx.run("ls -lta | awk '{print $3}'")
        res_travis_gid = ctx.run("ls -lta | awk '{print $4}'")

        ctx.config["run"]["env"]["CONTAINER_UID"] = "{}".format(res_travis_uid.stdout)
        ctx.config["run"]["env"]["CONTAINER_GID"] = "{}".format(res_travis_gid.stdout)

        if verbose >= 1:
            click.secho(
                "[test] CONTAINER_UID={}".format(
                    ctx.config["run"]["env"]["CONTAINER_UID"], fg=COLOR_SUCCESS
                )
            )
            click.secho(
                "[test] CONTAINER_GID={}".format(
                    ctx.config["run"]["env"]["CONTAINER_GID"], fg=COLOR_SUCCESS
                )
            )

    res_num_stopped_container = ctx.run(
        "docker ps -a| grep -v PORTS | grep Exited | awk '{print $1}' | wc -l"
    )

    if verbose >= 2:
        click.secho(
            "[test] _NUM_STOPPED_CONTAINER={}".format(
                res_num_stopped_container.stdout, fg=COLOR_SUCCESS
            )
        )

    ctx.config["run"]["env"]["_NUM_STOPPED_CONTAINER"] = "{}".format(
        res_num_stopped_container.stdout
    )

    _cmd_debug_stopped_containers = r"""
set -x

if [[ "${_NUM_STOPPED_CONTAINER}" -gt "0" ]]; then
    _CONTAINER_ID=$(docker ps -a -q --no-trunc | head -1)
    docker logs ${_CONTAINER_ID}
fi

set +x

    """

    _cmd_run_test = r"""
# -T Disable pseudo-tty allocation. By default `docker-compose exec` allocates a TTY.
time docker-compose -f docker-compose.ci.yml exec -T fake-medium-fastapi_ci /home/developer/app/.ci/pytest_runner.sh
    """

    if verbose >= 1:
        msg = "[test] cmd is: "
        click.secho(msg, fg=COLOR_SUCCESS)

        msg = "{}".format(_cmd_debug_stopped_containers)
        click.secho(msg, fg=COLOR_SUCCESS)

    ctx.run(_cmd_debug_stopped_containers)

    if verbose >= 1:
        msg = "[test] cmd to test container <untron8_ci> using pytest_runner is: "
        click.secho(msg, fg=COLOR_SUCCESS)

        msg = "{}".format(_cmd_run_test)
        click.secho(msg, fg=COLOR_SUCCESS)

        click.secho(
            "-T Disable pseudo-tty allocation. By default `docker-compose exec` allocates a TTY.",
            fg=COLOR_CAUTION,
        )

    ctx.run(_cmd_debug_stopped_containers)


# after-script
# - "docker-compose -f docker-compose.ci.yml kill -s SIGTERM"
# - "docker-compose -f docker-compose.ci.yml rm -f"

# after_success:
# - docker login -u $REGISTRY_USER -p $REGISTRY_PASS
# - docker push $CACHE_IMAGE:runtime-image | gnomon
# - _USER=$(ls -lta | awk '{print $3}')
# - _GROUP=$(ls -lta | awk '{print $4}')
# - docker ps -a
# - 'ls -lta'
# - 'sudo chown $_USER:$_GROUP -Rv *'
# - sudo mv .coverage .coverage.tests
# ################################################################################################
# # NOTE: https://coverage.readthedocs.io/en/coverage-4.5.1/changes.html?highlight=clean
# # Version 4.2b1 - 2016-07-04
# # BACKWARD INCOMPATIBILITY: the coverage combine command now ignores an existing .coverage data file. It used to include that file in its combining. This caused confusing results, and extra tox "clean" steps. If you want the old behavior, use the new coverage combine --append option.
# # ################################################################################################
# # NOTE: Version 4.5 - 2018-02-03
# # The coverage combine command used to always overwrite the data file, even when no data had been read from apparently combinable files. Now, an error is raised if we thought there were files to combine, but in fact none of them could be used. Fixes issue 629.
# - coverage combine
# # Coverage report contains Docker paths. We replace them, so that we can run Coveralls.
# - sed -i 's@\"/home/developer/app/@'"\"$(pwd)/"'@g' .coverage
# - coveralls

# before_cache:
# - _USER=$(ls -lta | awk '{print $3}')
# - _GROUP=$(ls -lta | awk '{print $4}')
# - 'sudo chown $_USER:$_GROUP -Rv $HOME/.cache/pip $HOME/.wheelhouse/'
