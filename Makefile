.DEFAULT_GOAL := help

PY_SRC := ytscraper/ tests/

.PHONY: build
build:  ## Build sdist and wheel.
	poetry build

.PHONY: bundle
bundle:  ## Build one-file executable.
	poetry run bash -c 'pyinstaller -F -n py-scraper -p $$VIRTUAL_ENV/lib/python3.8/site-packages ytscraper/__main__.py'

.PHONY: clean
clean: clean-tests  ## Delete temporary files.
	@rm -rf build 2>/dev/null
	@rm -rf dist 2>/dev/null
	@rm -rf src/ytscraper.egg-info 2>/dev/null
	@rm -rf .coverage* 2>/dev/null
	@rm -rf .pytest_cache 2>/dev/null
	@rm -rf pip-wheel-metadata 2>/dev/null

.PHONY: clean-tests
clean-tests:  ## Delete temporary tests files.
	@rm -rf tests/tmp/* 2>/dev/null


.PHONY: help
help:  ## Print this help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST) | sort

.PHONY: check
check: check-bandit check-black check-flake8 check-isort  ## Check it all!

.PHONY: check-bandit
check-bandit:  ## Check for security warnings in code using bandit.
	poetry run bandit -r src/

.PHONY: check-black
check-black:  ## Check if code is formatted nicely using black.
	poetry run black --check $(PY_SRC) --line-length 79

.PHONY: check-flake8
check-flake8:  ## Check for general warnings in code using flake8.
	poetry run flake8 $(PY_SRC)

.PHONY: check-isort
check-isort:  ## Check if imports are correctly ordered using isort.
	poetry run isort -c -rc $(PY_SRC)

.PHONY: check-mypy
check-mypy:  ## Check if code is correctly typed.
	poetry run mypy src

.PHONY: check-pylint
check-pylint:  ## Check for code smells using pylint.
	poetry run pylint $(PY_SRC)

.PHONY: lint
lint: lint-black lint-isort  ## Run linting tools on the code.

.PHONY: lint-black
lint-black:  ## Lint the code using black.
	poetry run black $(PY_SRC)

.PHONY: lint-isort
lint-isort:  ## Sort the imports using isort.
	poetry run isort -y -rc $(PY_SRC)

.PHONY: publish
publish:  ## Publish latest built version to PyPI.
	poetry publish

.PHONY: release
release:  ## Create a new release (commit, tag, push, build, publish).
	poetry version $(v)
	git add pyproject.toml CHANGELOG.md README.md
	git commit -m "Prepare release $(v)"
	git tag v$(v)
	git push
	git push --tags
	poetry build
	poetry publish

.PHONY: test
test: ## Run the tests using pytest.
	poetry run pytest tests/
