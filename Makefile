# SPDX-License-Identifier: LicenseRef-Databricks
# Derived from the Databricks FDE starter template; modified for genie-app-workshop. See NOTICE.
.DEFAULT_GOAL := help
.PHONY: help install lock check-lock lint format test

help:  ## Show this help
	@grep -hE '^[a-z-]+:.*?##' $(MAKEFILE_LIST) | awk 'BEGIN{FS=":.*?## "};{printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2}'

# uv works with whatever index your own uv config sets (e.g. a corporate PyPI proxy), but the
# committed uv.lock must reference only public PyPI so CI and cloners can install.
# Behind a proxy, put `export UV_FROZEN=1` in .envrc.local: syncs and runs then install from the
# lock without rewriting it. After `uv add <pkg>` (or editing pyproject.toml), run `make lock`.
PUBLIC_HOSTS = https://(pypi\.org|files\.pythonhosted\.org)

install:  ## Install dependencies, including dev
	uv sync --all-extras --all-groups

# Resolves through your configured index, then maps a PyPI proxy's URLs to the identical public
# files (proxies serve PyPI's own content-addressed /packages/... paths; hashes are unchanged).
lock:  ## Re-lock dependencies; the lock is rewritten to public PyPI URLs
	env -u UV_FROZEN uv lock
	sed -i.bak -E -e 's#registry = "https?://[^"]+"#registry = "https://pypi.org/simple"#g' \
	  -e 's#https?://[^/"]+/packages/#https://files.pythonhosted.org/packages/#g' uv.lock
	rm uv.lock.bak
	@$(MAKE) --no-print-directory check-lock

check-lock:  ## Fail if uv.lock references anything but public PyPI
	@bad=$$(grep -hoE 'https?://[^/"]+' uv.lock | grep -vxE '$(PUBLIC_HOSTS)' | sort -u); \
	if [ -n "$$bad" ]; then echo "non-public index hosts: $$bad (run make lock)" >&2; exit 1; fi

lint: check-lock  ## Check the lockfile, formatting, lint, and types
	uv run ruff format --check .
	uv run ruff check .
	uv run pyright

format:  ## Fix formatting and any auto-fixable lint
	uv run ruff format .
	uv run ruff check --fix .

test:  ## Run the tests with coverage. Needs no credentials and no workspace
	uv run pytest --cov=genie_app_workshop --cov-report=term-missing
