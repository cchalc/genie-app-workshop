# genie-app-workshop

Workshop project for building with Databricks Genie.

A Databricks App, deployed with a bundle, that asks a Genie space questions. The app is FastAPI
serving one page; its Genie call goes through `GenieClient` in `src/genie_app_workshop/`, which
the tests replace, so they need no workspace. It started from the app half of the FDE starter
template, without the template's React frontend or jobs.

## Install

Needs [uv](https://docs.astral.sh/uv/), [direnv](https://direnv.net/) and `make`.

```bash
direnv allow     # points uv at ~/.virtualenvs/genie-app-workshop (see .envrc)
make install     # uv sync, including dev tools
```

Per-developer secrets and overrides go in `.envrc.local`, which is gitignored.
uv uses whatever index your own uv config sets, a corporate PyPI proxy included. If you're
behind one, add `export UV_FROZEN=1` there so everyday syncs don't rewrite the public
`uv.lock`; see the comment above `install` in the [`Makefile`](Makefile).

## Usage

```bash
make lint        # ruff format check, ruff, pyright
make test        # pytest with coverage; needs no credentials and no workspace
make lock        # re-lock dependencies against public PyPI after editing pyproject.toml
make format      # apply formatting and auto-fixable lint
make help        # list targets
```

### Run the app

The app asks one Genie space, whose ID you supply. Nothing workspace-specific is committed: put
these in `.envrc.local`.

```bash
export GENIE_SPACE_ID=<space-id>               # read by the app when run locally
export BUNDLE_VAR_genie_space_id=<space-id>    # read by the bundle on validate and deploy
```

Every target that touches a workspace needs `PROFILE`, a Databricks CLI profile you choose.
There is no default.

```bash
make dev PROFILE=<profile>       # uvicorn on http://localhost:8000, using your CLI credentials
make validate PROFILE=<profile>  # databricks bundle validate (TARGET=dev by default)
make deploy PROFILE=<profile>    # deploy the bundle
make run PROFILE=<profile>       # start the deployed app
```

Once deployed, the app runs as its own service principal, which the bundle grants `CAN_RUN` on
the Genie space. That principal also needs access to the space's SQL warehouse and tables.
`TARGET=prod` deploys to the `prod` target, which first needs a service principal set where
`databricks.yml` is marked `SETUP`.

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
