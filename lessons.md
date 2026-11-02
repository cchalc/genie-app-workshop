# Lessons

Append-only, newest on top. Format: `### YYYY-MM-DD — title`, then What / Why it matters / Tags.

### 2026-11-01 — The FDE template's app can't import the package once deployed

**What:** the template's `resources/app.yml` sets `source_code_path: ../app`, so only `app/`
is uploaded and `from <package> import ...` in `app/backend/main.py` fails on the platform.
Pointing it at the bundle root (`..`) uploads `src/`, and Databricks Apps then installs the
project with `uv sync` from `pyproject.toml` + `uv.lock`. That's only when there's no
`requirements.txt`, which always wins. `uv sync` doesn't install extras, so app deps must be
main dependencies. Command and env go in the resource's `config` block rather than an
`app.yaml` at the root. The template's `name: ${bundle.name}-ui` is also invalid, because app
names reject underscores.
**Why it matters:** `make test` passes either way. Only a deploy shows it.
**Tags:** #databricks-apps #dabs

### 2026-11-01 — Starlette's TestClient wants httpx2

**What:** with current Starlette, `fastapi.testclient` on `httpx` raises
`StarletteDeprecationWarning`. `filterwarnings = ["error"]` turns that into a collection
error. The dev dependency is `httpx2`.
**Why it matters:** don't add `httpx` for FastAPI tests.
**Tags:** #fastapi #pytest

### 2026-11-01 — uv.lock got proxy URLs mid-session

**What:** twice, after a clean `make lock`, `uv.lock` was found holding proxy URLs again. I
couldn't reproduce it in isolation: `uv run`, `uv lock --check` and the gate all left it
clean. `make check-lock` (part of `make lint`) caught it both times.
**Why it matters:** run `make check-lock` right before committing, not just earlier in the
session.
**Tags:** #uv

### 2026-10-29 — uv.lock picks up the developer's default index

**What:** a user-level uv config pointing at a private PyPI mirror got recorded in `uv.lock`,
so CI couldn't install. Pinning public PyPI in `pyproject.toml` broke plain `uv` on a network
that only reaches the proxy, and exporting `UV_DEFAULT_INDEX` got persisted into
`pyproject.toml` by `uv add` (Isaac Review caught that). What works: leave the index to the
developer's uv config, set `UV_FROZEN=1` in `.envrc.local` so syncs don't rewrite the lock, and
let `make lock` rewrite proxy URLs to the identical public files (same `/packages/...` paths and
hashes). `make check-lock`, run by `make lint` and CI, guards the committed lock.
**Why it matters:** run `make lock` after any dependency change, and never commit a lock with
mirror URLs. `grep -o 'https://[^/"]*' uv.lock | sort -u` should show only pypi.org and
files.pythonhosted.org.
**Tags:** #uv #ci
