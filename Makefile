# app
runapp:
	uv run app/main.py

format:
	uv run ruff check --select I --fix
	uv run ruff format .

format_check:
	uv run ruff check

test:
	uv run pytest

type_check:
	uv run mypy . --explicit-package-bases

precommit:
	make format_check
	make test
	make type_check


migrate-create:
	alembic revision --autogenerate -m ${MES}

migrate-apply:
	alembic upgrade head