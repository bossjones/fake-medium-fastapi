import os

ROOT_DIR = os.path.dirname(__file__)
PROJECT_BIN_DIR = os.path.join(ROOT_DIR, "bin")
DATA_DIR = os.path.join(ROOT_DIR, "var")
SCRIPT_DIR = os.path.join(ROOT_DIR, "script")


# #--- User Defined Variable ---
# PACKAGE_NAME="fake-medium-fastapi"

# # Python version Used for Development
# PY_VER_MAJOR="3"
# PY_VER_MINOR="7"
# PY_VER_MICRO="4"

# #  Other Python Version You Want to Test With
# # (Only useful when you use tox locally)
# TEST_PY_VER3="3.7.4"

# # If you use pyenv-virtualenv, set to "Y"
# USE_PYENV="Y"

# # S3 Bucket Name
# DOC_HOST_BUCKET_NAME="NoBucket"


# #--- Derive Other Variable ---

# # Virtualenv Name
# VENV_NAME="${PACKAGE_NAME}_venv${PY_VER_MAJOR}${PY_VER_MINOR}${PY_VER_MICRO}"

# # Project Root Directory
# GIT_ROOT_DIR=${shell git rev-parse --show-toplevel}
# PROJECT_ROOT_DIR=${shell pwd}

# OS=${shell uname -s}

# ifeq (${OS}, Windows_NT)
# 		DETECTED_OS := Windows
# else
# 		DETECTED_OS := $(shell uname -s)
# endif


# # ---------

# # Windows
# ifeq (${DETECTED_OS}, Windows)
# 		USE_PYENV="N"

# 		VENV_DIR_REAL="${PROJECT_ROOT_DIR}/${VENV_NAME}"
# 		BIN_DIR="${VENV_DIR_REAL}/Scripts"
# 		SITE_PACKAGES="${VENV_DIR_REAL}/Lib/site-packages"
# 		SITE_PACKAGES64="${VENV_DIR_REAL}/Lib64/site-packages"

# 		GLOBAL_PYTHON="/c/Python${PY_VER_MAJOR}${PY_VER_MINOR}/python.exe"
# 		OPEN_COMMAND="start"
# endif


# # MacOS
# ifeq (${DETECTED_OS}, Darwin)

# ifeq ($(USE_PYENV), "Y")
# 		ARCHFLAGS="-arch x86_64"
# 		PKG_CONFIG_PATH=/usr/local/opt/libffi/lib/pkgconfig
# 		LDFLAGS="-L/usr/local/opt/openssl/lib"
# 		CFLAGS="-I/usr/local/opt/openssl/include"
# 		VENV_DIR_REAL="${HOME}/.pyenv/versions/${PY_VERSION}/envs/${VENV_NAME}"
# 		VENV_DIR_LINK="${HOME}/.pyenv/versions/${VENV_NAME}"
# 		BIN_DIR="${VENV_DIR_REAL}/bin"
# 		SITE_PACKAGES="${VENV_DIR_REAL}/lib/python${PY_VER_MAJOR}.${PY_VER_MINOR}/site-packages"
# 		SITE_PACKAGES64="${VENV_DIR_REAL}/lib64/python${PY_VER_MAJOR}.${PY_VER_MINOR}/site-packages"
# else
# 		ARCHFLAGS="-arch x86_64"
# 		PKG_CONFIG_PATH=/usr/local/opt/libffi/lib/pkgconfig
# 		LDFLAGS="-L/usr/local/opt/openssl/lib"
# 		CFLAGS="-I/usr/local/opt/openssl/include"
# 		# VENV_DIR_REAL="${PROJECT_ROOT_DIR}/${VENV_NAME}"
# 		# VENV_DIR_LINK="./${VENV_NAME}"
# 		VENV_DIR_REAL="${HOME}/.pyenv/versions/${PY_VERSION}/envs/${VENV_NAME}"
# 		VENV_DIR_LINK="${HOME}/.pyenv/versions/${VENV_NAME}"
# 		BIN_DIR="${VENV_DIR_REAL}/bin"
# 		SITE_PACKAGES="${VENV_DIR_REAL}/lib/python${PY_VER_MAJOR}.${PY_VER_MINOR}/site-packages"
# 		SITE_PACKAGES64="${VENV_DIR_REAL}/lib64/python${PY_VER_MAJOR}.${PY_VER_MINOR}/site-packages"
# endif
# 		ARCHFLAGS="-arch x86_64"
# 		PKG_CONFIG_PATH=/usr/local/opt/libffi/lib/pkgconfig
# 		LDFLAGS="-L/usr/local/opt/openssl/lib"
# 		CFLAGS="-I/usr/local/opt/openssl/include"

# 		GLOBAL_PYTHON="python${PY_VER_MAJOR}.${PY_VER_MINOR}"
# 		OPEN_COMMAND="open"
# endif


# # Linux
# ifeq (${DETECTED_OS}, Linux)
# 		USE_PYENV="N"

# 		VENV_DIR_REAL="${PROJECT_ROOT_DIR}/${VENV_NAME}"
# 		VENV_DIR_LINK="${PROJECT_ROOT_DIR}/${VENV_NAME}"
# 		BIN_DIR="${VENV_DIR_REAL}/bin"
# 		SITE_PACKAGES="${VENV_DIR_REAL}/lib/python${PY_VER_MAJOR}.${PY_VER_MINOR}/site-packages"
# 		SITE_PACKAGES64="${VENV_DIR_REAL}/lib64/python${PY_VER_MAJOR}.${PY_VER_MINOR}/site-packages"

# 		GLOBAL_PYTHON="python${PY_VER_MAJOR}.${PY_VER_MINOR}"
# 		OPEN_COMMAND="open"
# endif


# BASH_PROFILE_FILE = "${HOME}/.bash_profile"

# BIN_ACTIVATE="${BIN_DIR}/activate"
# BIN_PYTHON="${BIN_DIR}/python"
# BIN_PIP="${BIN_DIR}/pip"
# BIN_ISORT="${BIN_DIR}/isort"
# BIN_JINJA="${BIN_DIR}/jinja2"
# BIN_SPHINX_START="${BIN_DIR}/sphinx-quickstart"
# BIN_TWINE="${BIN_DIR}/twine"
# BIN_TOX="${BIN_DIR}/tox"
# BIN_JUPYTER="${BIN_DIR}/jupyter"
# BIN_PYTEST="${BIN_DIR}/pytest"

# RTD_DOC_URL="https://fake-medium-fastapi.readthedocs.io/index.html"


# PY_VERSION="${PY_VER_MAJOR}.${PY_VER_MINOR}.${PY_VER_MICRO}"

# https://github.com/bossjones/pocketsphinx-build/blob/master/pocketsphinx_build/build.py
# ENVRC_BUILD_TEMPLATE = """
# export CFLAGS = '{CFLAGS}'
# export PYTHON = 'python'
# export GSTREAMER = '1.0'
# export ENABLE_PYTHON3 = 'yes'
# export ENABLE_GTK = 'yes'
# export PYTHON_VERSION = '{PYTHON_VERSION}'
# export PATH = '{PATH}'
# export LD_LIBRARY_PATH = '{LD_LIBRARY_PATH}'
# export PYTHONPATH = '{PYTHONPATH}'
# export PKG_CONFIG_PATH = '{PKG_CONFIG_PATH}'
# export XDG_DATA_DIRS = '{XDG_DATA_DIRS}'
# export XDG_CONFIG_DIRS = '{XDG_CONFIG_DIRS}'
# export CC = 'gcc'
# export PROJECT_HOME = '{PROJECT_HOME}'
# export PYTHONSTARTUP = '{PYTHONSTARTUP}'
# """

# ENVRC_RUN_TEMPLATE = """
# export CFLAGS = '{CFLAGS}'
# export PYTHON = 'python'
# export GSTREAMER = '1.0'
# export ENABLE_PYTHON3 = 'yes'
# export ENABLE_GTK = 'yes'
# export PYTHON_VERSION = '{PYTHON_VERSION}'
# export PATH = '{PATH}'
# export LD_LIBRARY_PATH = '{LD_LIBRARY_PATH}'
# export PYTHONPATH = '{PYTHONPATH}'
# export PKG_CONFIG_PATH = '{PKG_CONFIG_PATH}'
# export XDG_DATA_DIRS = '{XDG_DATA_DIRS}'
# export XDG_CONFIG_DIRS = '{XDG_CONFIG_DIRS}'
# export CC = 'gcc'
# export PROJECT_HOME = '{PROJECT_HOME}'
# export PYTHONSTARTUP = '{PYTHONSTARTUP}'
# """
