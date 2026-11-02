<!-- SPDX-License-Identifier: LicenseRef-Databricks -->
<!-- Derived from the Databricks FDE starter template; modified for genie-app-workshop. See NOTICE. -->
# Agent guide

A Databricks App that asks a Genie space questions, deployed with a bundle. It started from the
FDE starter template's app half, without its React frontend or jobs. `make lint` and
`make test` pass. Keep them passing.

The Genie endpoint and its page are a placeholder for the workshop to build on. The layout,
the bundle, and the `GenieClient` seam are structure and they stay.

## Layout

| Path | Holds |
| :---- | :---- |
| `src/genie_app_workshop/` | The package. Logic lives here so tests can reach it |
| `src/genie_app_workshop/genie.py` | `GenieClient`, the seam between the app and Genie, and `WorkspaceGenie`, the SDK-backed one |
| `tests/` | Tests. No `__init__.py`, so pytest resolves them by path |
| `app/` | The HTTP layer and the page. Read `app/AGENTS.md` before changing it |
| `resources/app.yml` | The app resource: command, env, and the Genie space it may use |
| `databricks.yml` | The bundle: variables and the `dev` and `prod` targets |

Run `make help` for the commands. Use those rather than the underlying tools, because CI
calls the same targets and a change that works one way but not the other will fail late.

## Constraints

- Tests run with no credentials and no workspace. Anything reaching Databricks goes behind a
  seam a test can replace
- No workspace host, service principal ID, or token gets committed. They come from the
  environment, and a missing one should fail loudly
- The Genie space ID is per developer, not committed. It reaches the bundle as
  `BUNDLE_VAR_genie_space_id` and the app as `GENIE_SPACE_ID`
- Bundle targets (`validate`, `deploy`, `run`, `dev`) take `PROFILE=<name>` and have no
  default, so nothing runs against a workspace nobody chose
- Underscores for identifiers, hyphens for infrastructure. The package directory and
  `bundle.name` take underscores because Python and Unity Catalog both reject hyphens. The
  distribution name in `pyproject.toml` and the app name take hyphens, following PyPI and
  the Apps naming rules
- Line length 100, enforced by Ruff. Run `make format` rather than reformatting by hand
- Run `make lint` and `make test` before reporting work finished
