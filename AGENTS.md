# Agent guide

A working Databricks project, used as the starting point for new ones. `make lint`, `make test`,
and `make validate` pass as it stands. Keep them passing.

Distinguish structure from examples. The layout and config below are structure and they stay.
`notebooks/example.py`, `resources/jobs/example.yml`, and `table_name` with its test are
examples: they show the shape and should be replaced by real work rather than extended.

## Layout

| Path | Holds |
| :---- | :---- |
| `src/genie_app_workshop/` | The package. Logic lives here so tests can reach it |
| `tests/` | Tests. No `__init__.py`, so pytest resolves them by path |

Run `make help` for the commands. Use those rather than the underlying tools, because CI
calls the same targets and a change that works one way but not the other will fail late.

## Constraints

- Tests run with no credentials and no workspace. Anything reaching Databricks goes behind a
  seam a test can replace
- No workspace host, service principal ID, or token gets committed. They come from the
  environment, and a missing one should fail loudly
- Notebooks hold entrypoints, not logic. A bundle builds a wheel from `src/`, and a wheel
  cannot be built from notebooks
- Underscores for identifiers, hyphens for infrastructure. The package directory and
  `bundle.name` take underscores because Python and Unity Catalog both reject hyphens. The
  distribution name in `pyproject.toml` takes hyphens, following PyPI. Job resource keys and
  task keys are underscored, and task keys read `{action}_{target}`
- Line length 100, enforced by Ruff. Run `make format` rather than reformatting by hand
- Run `make lint` and `make test` before reporting work finished

## Starting a new project from this template

Delete this section once you reach the end of it. A derived repo should not carry instructions
for something that already happened.

1. Ask what the project is called, and whether it needs scheduled jobs, an app, or neither.
   Do not guess. Every step below depends on the answers
2. Copy this template into your target repo. From a sparse checkout of
   `reusable-ip-ai-components`, `reusable_ip/projects/dabs/repo_template/` is the directory to
   move; the README has the exact `git sparse-checkout` commands
3. Rename three fields to the project name, deleting the `SETUP` comment above each once done:
   - `src/genie_app_workshop/`, underscored
   - `name` in `pyproject.toml`, hyphenated
   - `bundle.name` in `databricks.yml`, underscored
4. Delete what the project does not need, which is one directory either way:
   - No UI: remove `app/` and `resources/app.yml`
   - No scheduled jobs: remove `notebooks/` and `resources/jobs/`
   - Neither: also remove `databricks.yml`, `resources/`, and the `validate` and `deploy`
     targets from the `Makefile`

   Removing `app/` leaves two inert references in `pyproject.toml`, the `app` extra and
   `app/backend` in pyright's include list. Neither breaks anything. Tidy them or leave them.
5. Find the remaining marker with `grep -rn SETUP .`. Prod needs a service principal, and you
   will not have one yet. Leave that marker where it is. Never write an ID you do not have
6. Wire in CI. The pipeline is not committed here; copy it from the shared CI/CD component as
   `.github/workflows/README.md` describes. `dependabot.yml` and `freshness.yml` already ship
   with the template
7. Verify: `make install && make lint && make test`. Add `make validate` once a Databricks CLI
   profile exists
8. Replace the README title and its `What this is` section, delete this section, then commit

Report anything still failing rather than a repo that looks finished. A work list beats a
green repo that quietly kept our names.
