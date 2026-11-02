<!-- SPDX-License-Identifier: LicenseRef-Databricks -->
<!-- Derived from the Databricks FDE starter template; modified for genie-app-workshop. See NOTICE. -->
# Working in app/

The HTTP layer and the page. Business logic belongs in `src/`, not here.

## Backend

`backend/main.py` does routing, validation, and serving the page. It imports from the package
and adds nothing of its own. A route that starts to contain logic means that logic belongs in
`src/` with a test.

Genie is reached only through the `genie` dependency. Tests replace it with
`app.dependency_overrides[genie]`, so they never reach a workspace. The real one is built on
first request, so the app starts without `GENIE_SPACE_ID` and fails loudly once asked.

## Page

`static/index.html` is one file with no build step. The template's React frontend was left out
until the workshop needs one; bring it back from the FDE starter template rather than growing
this file into one.

## Deploying

The app resource in `../resources/app.yml` points `source_code_path` at the bundle root, not
here, so the deployed app can import the package. The platform installs it from
`pyproject.toml` and `uv.lock`. There is no `app.yaml`: command and env sit in the resource's
`config` block.

## Local loop

`make dev PROFILE=<name>` from the repo root runs uvicorn on port 8000 with `GENIE_SPACE_ID`
from your environment.
