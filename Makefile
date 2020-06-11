.PHONY: pre-commit-install
pre-commit-install: ## install all pre-commit hooks
	pre-commit install -f --install-hooks
