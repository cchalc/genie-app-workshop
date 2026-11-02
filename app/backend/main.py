# SPDX-License-Identifier: LicenseRef-Databricks
# Derived from the Databricks FDE starter template; modified for genie-app-workshop. See NOTICE.
"""HTTP layer. Routing, validation, and serving the page. No business logic.

Anything worth testing lives in the package this imports from, where a test can reach it
without starting a server. Genie is reached through the `genie` dependency, which tests
override with a fake.
"""

from functools import cache
from pathlib import Path
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

from genie_app_workshop import GenieAnswer, GenieClient, WorkspaceGenie, ask
from genie_app_workshop.genie import space_id_from_env

PAGE = Path(__file__).resolve().parents[1] / "static" / "index.html"

app = FastAPI(title="genie-app-workshop")


class Question(BaseModel):
    question: str


@cache
def genie() -> GenieClient:
    """The real Genie client, built on first use so the app starts without a workspace."""
    return WorkspaceGenie(space_id_from_env())


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/genie/ask")
def ask_genie(body: Question, client: Annotated[GenieClient, Depends(genie)]) -> GenieAnswer:
    try:
        return ask(client, body.question)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@app.get("/", include_in_schema=False)
def page() -> FileResponse:
    return FileResponse(PAGE)
