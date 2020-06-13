.PHONY: pre-commit-install
pre-commit-install: ## install all pre-commit hooks
	pre-commit install -f --install-hooks

check-connection-postgres:
	poetry run scripts/check_connection.py
