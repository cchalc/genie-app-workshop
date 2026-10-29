# CI/CD Workflows

The CI pipeline is not committed here. Copy it from the CI/CD component for your platform of
choice and resolve the `SETUP TODO` items:

- **GitHub Actions** — [`components/cicd/github_actions_pipeline/`](../../../../components/cicd/github_actions_pipeline/)

See the [CI/CD component README](../../../../components/cicd/README.md) for setup instructions,
required secrets, and design rationale. The component's `ci.yml` runs the same `make` targets
you run locally (`make lint`, `make test`, `make validate`), so porting to another platform
means rewriting a few lines of YAML rather than reimplementing the pipeline.

`freshness.yml` (in this directory) and `dependabot.yml` (in `.github/`) are separate from the
CI/CD component and stay with the template. Dependabot raises grouped version bumps weekly;
`freshness.yml` re-resolves everything to its newest allowed version on a schedule and runs the
gates, catching breakage that arrives without a version bump.
