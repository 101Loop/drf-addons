.PHONY: clean-pyc clean-build docs clean

VIRTUALENV = virtualenv --python=python3
PYTHON = $(VENV)/bin/python
VENV := $(shell echo $${VIRTUAL_ENV-.venv})

TEST_FLAGS=--verbosity=2
COVER_FLAGS=--source=drf_user

help:
	@echo "install - install all requirements including for testing"
	@echo "install-quite - same as install but pipes all output to /dev/null"
	@echo "clean - remove all artifacts"
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "clean-test - remove test and coverage artifacts"
	@echo "clean-test-all - remove all test-related artifacts including tox"
	@echo "lint - check style with flake8"
	@echo "format - format code with black"
	@echo "test - run tests quickly with the default Python"
	@echo "test-coverage - run tests with coverage report"
	@echo "check - run all necessary steps to check validity of project"
	@echo "dist - package"

install:
	pip install -r dev_requirements.txt
	pip install -e .
	pre-commit install


install-quite:
	pip install -r dev_requirements.txt > /dev/null

clean: clean-build clean-pyc clean-test-all

clean-build:
	@rm -rf build/
	@rm -rf dist/
	@rm -rf *.egg-info

clean-pyc:
	-@find . -name '*.pyc' -follow -print0 | xargs -0 rm -f
	-@find . -name '*.pyo' -follow -print0 | xargs -0 rm -f
	-@find . -name '__pycache__' -type d -follow -print0 | xargs -0 rm -rf

clean-test:
	rm -rf .coverage coverage*
	rm -rf tests/.coverage test/coverage*
	rm -rf htmlcov/

lint:
	flake8  --exclude=*/migrations/* --max-line-length 88 drfaddons

format:
	black --exclude .+/migrations/.+\.py drfaddons

test:
	$(PYTHON) -m pytest --disable-pytest-warnings --ds=tests.settings --cov=drfaddons tests/

test-coverage: clean-test
	$(PYTHON) -m pytest --disable-pytest-warnings --ds=tests.settings --cov=drfaddons tests/ --cov-report html


check: clean-build clean-pyc clean-test lint format test


dist: clean
	python setup.py sdist
	ls -l dist
