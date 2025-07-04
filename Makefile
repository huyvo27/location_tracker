# Variables
ENV_FILE = .env
APP_MODULE = app.main:app
HOST = 0.0.0.0
PORT = 8000

# Commands
install:
	@poetry install --only main

install-dev:
	@poetry install --with dev

install-test:
	@poetry install --with test

run:
	@uvicorn $(APP_MODULE) --reload --host $(HOST) --port $(PORT) --env-file $(ENV_FILE)

format:
	@black .
	@isort .

lint:
	@flake8 .

check:
	@black --check .
	@isort --check-only .
	@flake8 .

test: unit-test integration-test

unit-test:
	@echo "\033[1;34m [Unit Tests] Running unit tests...\033[0m"
	@pytest tests/unit

integration-test:
	@echo "\033[1;32m [Integration Tests] Running integration tests...\033[0m"
	@pytest tests/integration

migrate:
	@alembic upgrade head

makemigrations:
	@alembic revision --autogenerate -m "Auto migration"

clean-pyc:
	@find . -name "*.pyc" -delete
	@find . -name "__pycache__" -delete

clean:
	@rm -rf __pycache__ .pytest_cache .mypy_cache *.pyc

