<!-- SPDX-License-Identifier: LicenseRef-Databricks -->
<!-- Derived from the Databricks FDE starter template; modified for genie-app-workshop. See NOTICE. -->
# Agent guide

A Python package with tests, started from the FDE starter template with no app, jobs, or bundle.
`make lint` and `make test` pass. Keep them passing.

Distinguish structure from examples. The layout and config below are structure and they stay.
`table_name` with its test is an example: it shows the shape and should be replaced by real work
rather than extended.

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
- Underscores for identifiers, hyphens for infrastructure. The package directory (and any
  future `bundle.name`) takes underscores because Python and Unity Catalog both reject hyphens.
  The distribution name in `pyproject.toml` takes hyphens, following PyPI
- Line length 100, enforced by Ruff. Run `make format` rather than reformatting by hand
- Run `make lint` and `make test` before reporting work finished
