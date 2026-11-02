# Changelog

All notable user-visible changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added
- A Databricks App that asks a Genie space questions: a FastAPI endpoint
  (`POST /api/genie/ask`) and a page to ask from, deployed with a `databricks.yml` bundle.
  The Genie space comes from `GENIE_SPACE_ID` / `BUNDLE_VAR_genie_space_id`, and
  `make dev`/`validate`/`deploy`/`run` take an explicit `PROFILE`.
- `genie_app_workshop` Python package with tests, `make install`/`lint`/`format`/`test`, and
  CI running the same gate, scaffolded from the FDE starter template.
- Dev standards for contributors and coding agents: `CLAUDE.md`, the ai-kitchen `core` and
  `bespoke` plugins, and an out-of-source uv venv via `.envrc`.
- MIT license for the project, with the files derived from the FDE starter template kept under
  the Databricks License, as listed in `NOTICE`.
