.PHONY: deps install clean tests serve lint

ENV=.env
SYS_PYTHON=$(shell which python3)
SYS_PYTHON_VERSION=$(shell ${SYS_PYTHON} -V | cut -d " " -f 2 | cut -c1-3)
SITE_PACKAGES=${ENV}/lib/python${SYS_PYTHON_VERSION}/site-packages
IN_ENV=. ${ENV}/bin/activate; export PYTHONPATH=.;
MANAGE=python scripts/manage.py
PYTHONPATH=export PYTHONPATH=.

default: deps

${ENV}:
	@echo "Creating Python ${SYS_PYTHON_VERSION} environment based on ${SYS_PYTHON}..." >&2
	@${SYS_PYTHON} -m venv ${ENV}
	@echo "Updating pip..." >&2
	@${IN_ENV} pip install -U pip

${SITE_PACKAGES}/django: ${ENV}
	@echo "Installing Python dependencies..."
	@${IN_ENV} pip install -qqqr requirements.txt

${SITE_PACKAGES}/flake8: ${ENV}
	@echo "Installing linter..."
	@${IN_ENV} pip install flake8

deps: ${SITE_PACKAGES}/django

install: default
	@pip install -e .

serve: default
	@${IN_ENV} ${MANAGE} runserver

tests: default
	@${IN_ENV} ${MANAGE} test rheia

lint: ${ENV} ${SITE_PACKAGES}/flake8
	@${IN_ENV} flake8 rheia/ --exclude .env

clean:
	@echo "Removing Python environment..."
	@rm -rf ${ENV}
	@echo "Removing Python byte-compiled files..."
	@find . -name "*.pyc" -exec rm {} \;
