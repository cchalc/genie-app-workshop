# Checkpoint

**Last session:** 2026-10-29 — repo bootstrapped with the project-startup skill, made public,
and reviewed with Isaac Review.

**Current state:** branch `cchalc/project-setup` (not pushed):
- dev standards: `.claude/settings.json` → `core` + `bespoke` @ ai-kitchen, CLAUDE.md, committed `.envrc`
- FDE starter template merged as a package + tests only project (no app, jobs, or bundle)
- `uv.lock` holds only public PyPI URLs; `make lock` re-locks through your own uv index (the proxy) and rewrites them
- CI: lint, test with coverage, whitespace, offline link check
- MIT license; template-derived files stay under the Databricks License (`NOTICE`)

The gate (`make lint && make test`) is green.

**Next action (resume point):** push the branch, open the PR (pull-requests), watch CI. Then
replace the template example (`table_name`) with the first real workshop module.

**Blockers:** none. On this machine pypi.org is blocked; uv goes through the Databricks proxy
(`~/.config/uv/uv.toml`), and `.envrc.local` sets `UV_FROZEN=1` (see the Makefile).
