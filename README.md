# genie-app-workshop

## What this is

The FDE starter template: a working Databricks project meant to be copied and renamed rather
than read and reimplemented. `make lint`, `make test`, and `make validate` all pass as it
stands. Wire in the CI/CD component (see below) to keep them passing on every push.

Two kinds of file live here. **Structure** is the layout and the config, and it stays.
**Examples** are `notebooks/example.py`, `resources/jobs/example.yml`, `app/`, and the
`table_name` function with its test. They exist to show the shape and are meant to be replaced by real work
rather than built on.

Point a coding agent at `AGENTS.md`, which carries a step-by-step sequence for turning this
into your project. By hand, the three renames below take a minute.

Replace this section and the title once the repo is yours.

## Starting a new project

Three name fields identify a project. Change all three:

| What | Where |
| :---- | :---- |
| Package directory | `src/genie_app_workshop/` |
| Distribution name | `name` in `pyproject.toml` |
| Bundle name | `bundle.name` in `databricks.yml`, underscored |

Imports move with the directory and the wheel build reads the distribution name, so nothing
else follows from the name. Lint, tests, and `bundle validate` fail while any of the three
still says `genie_app_workshop`.

One further edit is marked `SETUP`, and `grep -rn SETUP .` finds it: a service principal,
needed only when you deploy to prod. No workspace host appears anywhere, because that comes
from your Databricks CLI profile.

Spark is not a dependency, because the Databricks runtime provides it. To run Spark code on
your own machine, add `pyspark` for hermetic unit tests, or `databricks-connect` to execute
against a cluster. They conflict, so pick one.

The repo covers two shapes and you delete the half you do not need: `app/` for a project with
no UI, or `notebooks/` and `resources/jobs/` for one with no scheduled jobs. FastAPI sits in an
optional dependency group, so a jobs-only project never installs a web framework.

```bash
make install
make test      # passes with no credentials and no workspace
make validate  # checks the bundle against your profile
```

The bundle requires Databricks CLI 1.0 or newer. Upgrading from 0.x moves OAuth tokens into the
OS keychain, so run `databricks auth login` once per profile afterwards.

Run `make help` for the rest. The Makefile is the task interface for local work, and the
CI/CD component runs the same gates on every push.

## CI/CD

The CI pipeline is not committed in the template. Copy it from the shared
[CI/CD component](../../../components/cicd/) — `.github/workflows/README.md` has the pointer
and the relative paths. The component runs the same `lint`, `test`, and `bundle validate`
gates you run locally. `dependabot.yml` and `.github/workflows/freshness.yml` ship with the
template and keep dependencies current independently of the CI/CD component.

## Why it is shaped this way

**`src/` and `notebooks/` are separate.** A bundle builds a wheel from `src/`, and a wheel
cannot be built from notebooks. Keeping them apart means logic lives in a tested package and
notebooks stay thin entrypoints that call into it. `notebooks/example.py` shows the shape.

**Tests run with no credentials.** A suite that needs a workspace is a suite nobody runs, so
it stops being run, and then it stops passing. Anything reaching Databricks belongs behind a
seam a test can replace.

**No workspace host or service principal ID is committed.** Both come from your environment.
A template carrying somebody else's host deploys your project into their workspace.

**Two targets, and only one needs configuring.** `dev` works as it stands. `prod` needs a
service principal, marked `SETUP` in `databricks.yml`. Add `staging` when you have something
to stage.

**The frontend is pre-wired, and the choices are not ours alone.** Tailwind 4, Vite, React,
Vitest, and Lucide are what Databricks AppKit uses. shadcn/ui components arrive through its CLI
rather than hand-written. TanStack Query is the one place we differ from AppKit, which uses
custom hooks: Query removes more code than it adds. Diagramming, charts, and data grids are left
out, being features rather than toolchain.

**CI lives in a shared component, not the template.** The [CI/CD component](../../../components/cicd/)
runs the same gates against every project that copies it, so a fix to the pipeline reaches all
of them. Porting to GitLab or Azure DevOps means swapping one component for another rather than
reimplementing the pipeline.

**Dependencies stay current through two mechanisms.** Dependabot raises version bumps weekly,
grouped so a week arrives as two pull requests. A scheduled job (`freshness.yml`) resolves
everything to its newest allowed version and runs the gates, which catches breakage that
arrives without a version bump. TypeScript is held at 6 because `typescript-eslint` does not
yet support 7.

**The lint rules are the ones nobody argues with.** Adding rules to a green repo is easy.
Removing them once CI is red is not.
