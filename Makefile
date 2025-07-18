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
	@poetry install --no-root --no-interaction --no-ansi --with test

install-check:
	@poetry install --no-root --no-interaction --no-ansi --only check

run:
	@uvicorn $(APP_MODULE) --reload --host $(HOST) --port $(PORT) --env-file $(ENV_FILE)

format:
	@poetry run black .
	@poetry run isort .

lint:
	@poetry run flake8 .

check:
	@poetry run black --check .
	@poetry run isort --check-only .
	@poetry run flake8 .

test: unit-test integration-test

unit-test:
	@echo "\033[1;34m [Unit Tests] Running unit tests...\033[0m"
	@poetry run pytest tests/unit --cov=app --disable-warnings -v

integration-test:
	@echo "\033[1;32m [Integration Tests] Running integration tests...\033[0m"
	@poetry run pytest tests/integration --disable-warnings -v

migrate:
	@poetry run alembic upgrade head

makemigrations:
	@poetry run alembic revision --autogenerate -m "Auto migration"

clean-pyc:
	@find . -name "*.pyc" -delete
	@find . -name "__pycache__" -delete

clean:
	@rm -rf __pycache__ .pytest_cache .mypy_cache *.pyc

