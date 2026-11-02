"""Asking a Genie space a question.

`GenieClient` is the seam. The app talks to Genie only through it, so tests pass a fake and
never reach a workspace. `WorkspaceGenie` is the real one, backed by the Databricks SDK.
"""

import os
from dataclasses import dataclass
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from databricks.sdk import WorkspaceClient
    from databricks.sdk.service.dashboards import GenieMessage

SPACE_ID_ENV = "GENIE_SPACE_ID"
MAX_QUESTION_LENGTH = 2000


@dataclass(frozen=True)
class GenieAnswer:
    """What the app shows for one question: Genie's reply and the SQL it ran, if any."""

    text: str
    sql: str | None
    conversation_id: str


class GenieClient(Protocol):
    def ask(self, question: str) -> GenieAnswer: ...


def space_id_from_env() -> str:
    """The Genie space to ask, from the environment. Missing fails loudly rather than late."""
    space_id = os.environ.get(SPACE_ID_ENV, "").strip()
    if not space_id:
        raise RuntimeError(f"{SPACE_ID_ENV} is not set; point it at a Genie space ID")
    return space_id


def clean_question(question: str) -> str:
    """The question as sent to Genie: trimmed, non-empty, and within the length limit."""
    question = question.strip()
    if not question:
        raise ValueError("question is required")
    if len(question) > MAX_QUESTION_LENGTH:
        raise ValueError(f"question is longer than {MAX_QUESTION_LENGTH} characters")
    return question


def ask(client: GenieClient, question: str) -> GenieAnswer:
    """Ask `client` a validated question."""
    return client.ask(clean_question(question))


def answer_from_message(message: "GenieMessage") -> GenieAnswer:
    """Flatten a Genie message into the reply text and the first generated query."""
    texts: list[str] = []
    sql: str | None = None
    for attachment in message.attachments or []:
        if attachment.text and attachment.text.content:
            texts.append(attachment.text.content)
        if attachment.query:
            if attachment.query.description:
                texts.append(attachment.query.description)
            if sql is None and attachment.query.query:
                sql = attachment.query.query
    if message.error and message.error.error:
        texts.append(f"Genie reported an error: {message.error.error}")
    return GenieAnswer(
        text="\n\n".join(texts) or "Genie returned no text.",
        sql=sql,
        conversation_id=message.conversation_id,
    )


class WorkspaceGenie:
    """`GenieClient` backed by a workspace. Credentials come from the SDK's own config chain:
    a CLI profile locally, the app's service principal once deployed."""

    def __init__(self, space_id: str, workspace: "WorkspaceClient | None" = None) -> None:
        self.space_id = space_id
        self._workspace = workspace

    @property
    def workspace(self) -> "WorkspaceClient":
        if self._workspace is None:
            from databricks.sdk import WorkspaceClient

            self._workspace = WorkspaceClient()
        return self._workspace

    def ask(self, question: str) -> GenieAnswer:
        message = self.workspace.genie.start_conversation_and_wait(self.space_id, question)
        return answer_from_message(message)
