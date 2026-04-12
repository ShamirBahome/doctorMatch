# Run from this directory:
VENV ?= venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
FLASK := $(VENV)/bin/flask
PORT ?= 5000
HOST ?= 127.0.0.1

.PHONY: help venv install run dev gunicorn seed clean clean-venv

help:
	@echo "Targets:"
	@echo "  make install    Create venv (if needed) and pip install requirements"
	@echo "  make run        Development server (Flask debug, port $(PORT))"
	@echo "  make dev        Same as run"
	@echo "  make gunicorn   Production server (override HOST/PORT as needed)"
	@echo "  make seed       Load sample doctors/users/reviews (SQLite)"
	@echo "  make clean      Remove __pycache__"
	@echo "  make clean-venv Remove venv directory"

venv:
	@test -d "$(VENV)" || python3 -m venv "$(VENV)"

install: venv
	$(PIP) install -U pip
	$(PIP) install -r requirements.txt

run dev: install
	$(FLASK) --app app run --debug --host "$(HOST)" --port "$(PORT)"

gunicorn: install
	$(VENV)/bin/gunicorn -w 2 -b "$(HOST):$(PORT)" "app:app"

seed: install
	$(PYTHON) -c "from app import app; from seed_data import seed_database; ctx = app.app_context(); ctx.push(); seed_database()"

clean:
	rm -rf __pycache__
	rm -rf templates/__pycache__ 2>/dev/null || true

clean-venv:
	rm -rf "$(VENV)"
