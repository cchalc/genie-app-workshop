# genie-app-workshop

Workshop project for building with Databricks Genie.

A Python package with tests, started from the FDE starter template as a package-only project
(no Databricks App, jobs, or bundle yet). `table_name` in `src/genie_app_workshop/` is the
template's example and is meant to be replaced with real workshop code.

## Install

Needs [uv](https://docs.astral.sh/uv/), [direnv](https://direnv.net/) and `make`.

```bash
direnv allow     # points uv at ~/.virtualenvs/genie-app-workshop (see .envrc)
make install     # uv sync, including dev tools
```

Per-developer secrets and overrides go in `.envrc.local`, which is gitignored.

## Usage

```bash
make lint        # ruff format check, ruff, pyright
make test        # pytest; needs no credentials and no workspace
make format      # apply formatting and auto-fixable lint
make help        # list targets
```

To add a Databricks App or scheduled jobs later, bring back that half of the FDE starter
template (`app/` + `resources/app.yml`, or `notebooks/` + `resources/jobs/`) with a
`databricks.yml` bundle.

## Contributing

Agents and humans follow [`CLAUDE.md`](CLAUDE.md) and [`AGENTS.md`](AGENTS.md). Branch,
commit, PR and review conventions come from the `core` and `bespoke` plugins in the
[ai-kitchen](https://github.com/cchalc/ai-kitchen) marketplace, which `.claude/settings.json`
enables for this repo. CI ([`.github/workflows/check.yml`](.github/workflows/check.yml)) runs
the same `make lint` and `make test`. Record user-visible changes in
[`CHANGELOG.md`](CHANGELOG.md).

## License

[MIT](LICENSE) © 2026 Christopher Chalcraft, except for the files derived from the Databricks
FDE starter template. Those stay under the [Databricks License](LICENSES/LicenseRef-Databricks.txt);
[`NOTICE`](NOTICE) lists them.
