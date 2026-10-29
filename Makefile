# SPDX-License-Identifier: LicenseRef-Databricks
# Derived from the Databricks FDE starter template; modified for genie-app-workshop. See NOTICE.
.DEFAULT_GOAL := help
.PHONY: help install lock lint format test

help:  ## Show this help
	@grep -hE '^[a-z-]+:.*?##' $(MAKEFILE_LIST) | awk 'BEGIN{FS=":.*?## "};{printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2}'

install:  ## Install dependencies, including dev
	uv sync --all-extras --all-groups

# uv.lock must point at public PyPI so CI and cloners can install. If your network only reaches
# a PyPI mirror, set these in .envrc.local (base URL of the mirror, no trailing slash):
#   export PYPI_MIRROR=https://<mirror>
#   export UV_DEFAULT_INDEX=$PYPI_MIRROR/simple/  UV_FROZEN=1
# Day-to-day syncs then install from the lock without rewriting it, and `make lock` resolves
# through the mirror and rewrites its URLs to the identical public PyPI files.
lock:  ## Re-lock dependencies against public PyPI (via PYPI_MIRROR if set)
	@if [ -n "$$PYPI_MIRROR" ]; then \
	  env -u UV_FROZEN UV_DEFAULT_INDEX="$$PYPI_MIRROR/simple/" uv lock && \
	  sed -i.bak -e "s#$$PYPI_MIRROR/simple/#https://pypi.org/simple#g" \
	    -e "s#$$PYPI_MIRROR/packages/#https://files.pythonhosted.org/packages/#g" uv.lock && \
	  rm uv.lock.bak; \
	else env -u UV_FROZEN uv lock; fi
	@! grep -q "$${PYPI_MIRROR:-no-mirror-set}" uv.lock || { echo "uv.lock still references the mirror" >&2; exit 1; }

lint:  ## Check formatting, lint, and types
	uv run ruff format --check .
	uv run ruff check .
	uv run pyright

format:  ## Fix formatting and any auto-fixable lint
	uv run ruff format .
	uv run ruff check --fix .

test:  ## Run the tests with coverage. Needs no credentials and no workspace
	uv run pytest --cov=genie_app_workshop --cov-report=term-missing
