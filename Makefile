.PHONY: test install dev venv clean
.ONESHELL:

VENV=.venv
PY_VER=python3.11
PYTHON=./$(VENV)/bin/$(PY_VER)
PIP_INSTALL=$(PYTHON) -m pip install
BASIC=pip setuptools wheel

test:
	$(PYTHON) -m unittest discover

install: venv
	source $(VENV)/bin/activate
	$(PIP_INSTALL) -U $(BASIC)
	$(PIP_INSTALL) .

dev: venv
	source $(VENV)/bin/activate
	$(PIP_INSTALL) -U $(BASIC)
	$(PIP_INSTALL) -e .[dev]
	pre-commit install

venv:
	test -d $(VENV) || $(PY_VER) -m venv $(VENV)

clean:
	rm -r $(VENV)
	find -iname "*.pyc" -delete
