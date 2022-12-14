PY = python3
VENV = venv
BIN = $(VENV)/bin

TEST_DIR = tests

ifeq ($(OS), Windows_NT)
	BIN = $(VENV)/Scripts
	PY = python
endif

$(VENV): 
	$(PY) -m venv $(VENV)
	$(BIN)/pip install --upgrade -r requirements.txt
	$(BIN)/pip install -e .
	touch $(VENV)

.PHONY: test clean init dist docs

init: $(VENV)

test: $(VENV) init
	$(BIN)/python3 -m unittest discover

dist:
	$(BIN)/python3 setup.py sdist bdist_wheel

clean: 
	rm -rf tests/build
	rm -rf dist
	find . -type f -name *.pyc -delete
	find . -type d -name __pycache__ -delete