# genie-app-workshop

Workshop project for building with Databricks Genie.

Layout, commands and constraints live in `AGENTS.md`; all of it applies here. This file adds
the session protocol and dev standards.

## Living docs (read in order at session start)
1. `checkpoint.md` — where the last session left off
2. `tasks.md` — in progress, next, backlog, done
3. `lessons.md` — append-only learnings (consult when stuck)

At session end: **overwrite** `checkpoint.md`, update `tasks.md` (move finished items to Done
with date + SHA), and **append** surprises to `lessons.md` (newest on top). If context runs
short mid-task, write the checkpoint first, then continue.

## Workflow
- Gate: `make lint && make test`. CI runs the same targets — run them before reporting work
  finished.
- Dev standards come from the `ai-kitchen` plugins, enabled for this repo in
  `.claude/settings.json`. Follow them:

| Skill | Use it when |
|---|---|
| `core:committing-work` | Naming a branch, writing or signing a commit, fixups |
| `core:pull-requests` | Opening, filling, or merging a PR |
| `core:reviewing-prs` | Reviewing someone else's PR |
| `core:code-testing` | Adding or changing tests; regression test before a bug fix |
| `core:ponytail-fix` | The gate or CI is red |
| `bespoke:setup-ci` | Changing CI or branch protection |
| `bespoke:writing-readmes` | Editing a README |
| `bespoke:changelog` | Recording user-visible changes in `CHANGELOG.md` |
| `bespoke:gitignore` | Adding ignore rules |

## Python
- Out-of-source venv at `~/.virtualenvs/genie-app-workshop`, set by the committed `.envrc`
  (one venv per checkout, so worktrees never share one). Run `direnv allow` once.
- `uv add <pkg>` for deps, then `make lock`; `uv run <cmd>` to run. Never `pip install`
  outside the venv.
- uv resolves through the developer's own index config (here, the Databricks PyPI proxy in
  `~/.config/uv/uv.toml`, with `UV_FROZEN=1` in `.envrc.local`). Don't pin an index in
  `pyproject.toml` or export `UV_DEFAULT_INDEX`.
- `uv.lock` must reference only public PyPI (`pypi.org`, `files.pythonhosted.org`), or CI and
  cloners can't install. `make lock` re-locks and rewrites proxy URLs to the identical public
  files; `make lint` runs `check-lock`, which fails on any other host.
- Secrets and per-developer overrides go in `.envrc.local` (gitignored). Never commit
  credentials, workspace hosts, or tokens.
