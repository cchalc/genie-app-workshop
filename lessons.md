# Lessons

Append-only, newest on top. Format: `### YYYY-MM-DD — title`, then What / Why it matters / Tags.

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
