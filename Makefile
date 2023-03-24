# copied from https://github.com/ashleve/lightning-hydra-template/edit/main/Makefile

format: ## Run pre-commit hooks
	poetry run pre-commit run -a

sync: ## Merge changes from main branch to your current branch
	git fetch
	git pull

test: ## Run not slow tests
	poetry run pytest -v

test-full: ## Run all tests
	poetry run pytest -v --slow
