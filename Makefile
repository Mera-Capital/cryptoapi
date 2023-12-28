py := poetry run
package_dir := src

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: install
install: ## Install package with dependencies
	poetry install --with dev

.PHONY: lint
lint: ## Lint code
	$(py) flake8 $(package_dir) --exit-zero
	$(py) pylint $(package_dir) --exit-zero
	$(py) mypy $(package_dir) || true
