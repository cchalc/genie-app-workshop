# Tasks

Rolling work list. Updated each session.

## In Progress

## Next

- [ ] Push `cchalc/project-setup`, open the PR, and confirm all CI jobs go green.
- [ ] Open the `cchalc/app-scaffold` PR (stacked on #1) and confirm CI goes green.
- [ ] `make validate PROFILE=<name>` with a real Genie space ID, then a first `dev` deploy to
      confirm the platform's `uv sync` installs the package and the app starts.
- [ ] Genie answers return text and SQL only: fetch query results
      (`get_message_attachment_query_result`) and support follow-ups in a conversation.

## Backlog

- [ ] Branch protection on `main` requiring the `lint` and `test` checks (setup-ci).
- [ ] Keep dev tools out of the deployed app: the platform's `uv sync` installs the default
      `dev` group (pytest, pyright, ruff) unless told otherwise.
- [ ] Bring back the template's React frontend if the page outgrows `app/static/index.html`.

## Done (recent)

- [x] Databricks App scaffold: Genie-backed FastAPI app, bundle, `table_name` replaced (2026-11-01, 3d2aeee)

- [x] Bootstrap repo: dev standards, uv env, FDE template (package + tests), CI (2026-10-29)
- [x] Make repo public; MIT + Databricks License NOTICE; public-PyPI lockfile (2026-10-29)
