# Checkpoint

**Last session:** 2026-11-01. Added the Databricks App scaffold on `cchalc/app-scaffold`,
stacked on `cchalc/project-setup` (PR #1, not merged).

**Current state:**
- `src/genie_app_workshop/genie.py`: `GenieClient` seam, `WorkspaceGenie` (databricks-sdk),
  answer flattening, `GENIE_SPACE_ID` from env. `table_name` is gone
- `app/backend/main.py`: FastAPI, `POST /api/genie/ask`, `/api/health`, and the static page
  in `app/static/index.html`. Tests override the `genie` dependency
- `databricks.yml` + `resources/app.yml`: app `genie-app-workshop` with a `genie_space`
  resource (`CAN_RUN`) from `var.genie_space_id`, which has no default. `source_code_path`
  is the bundle root, so the platform installs the package via `uv sync`
- Makefile: `dev`/`validate`/`deploy`/`run` require `PROFILE=<name>`

The gate (`make lint && make test`) is green, with 20 tests and 100% coverage of the package
and `app/`. `databricks bundle validate` has not been run yet, because no profile was chosen.

**Next action (resume point):** after review, run `make validate PROFILE=<name>` with
`BUNDLE_VAR_genie_space_id` set, then deploy to `dev` and check the app starts. See
tasks.md.

**Blockers:** none. pypi.org is blocked on this machine, so uv goes through the Databricks
proxy. Run `make lock` after dependency changes and `make check-lock` before committing.
