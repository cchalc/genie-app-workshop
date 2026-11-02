from types import SimpleNamespace
from typing import Any, cast

import pytest
from databricks.sdk.service.dashboards import (
    GenieAttachment,
    GenieMessage,
    GenieQueryAttachment,
    MessageError,
    TextAttachment,
)

from genie_app_workshop import GenieAnswer, WorkspaceGenie, ask
from genie_app_workshop.genie import (
    MAX_QUESTION_LENGTH,
    SPACE_ID_ENV,
    answer_from_message,
    clean_question,
    space_id_from_env,
)


def message(*attachments: GenieAttachment, error: str | None = None) -> GenieMessage:
    return GenieMessage(
        id="m1",
        message_id="m1",
        space_id="s1",
        conversation_id="c1",
        content="question",
        attachments=list(attachments),
        error=MessageError(error=error) if error else None,
    )


class FakeGenie:
    def __init__(self) -> None:
        self.questions: list[str] = []

    def ask(self, question: str) -> GenieAnswer:
        self.questions.append(question)
        return GenieAnswer(text="42", sql=None, conversation_id="c1")


class FakeGenieAPI:
    def __init__(self, reply: GenieMessage) -> None:
        self.reply = reply
        self.calls: list[tuple[str, str]] = []

    def start_conversation_and_wait(self, space_id: str, content: str) -> GenieMessage:
        self.calls.append((space_id, content))
        return self.reply


def test_ask_sends_the_trimmed_question() -> None:
    genie = FakeGenie()
    assert ask(genie, "  how many orders?  ").text == "42"
    assert genie.questions == ["how many orders?"]


@pytest.mark.parametrize("blank", ["", "   ", "\n\t"])
def test_rejects_a_blank_question(blank: str) -> None:
    with pytest.raises(ValueError, match="required"):
        clean_question(blank)


def test_question_length_limit_is_inclusive() -> None:
    assert clean_question("x" * MAX_QUESTION_LENGTH) == "x" * MAX_QUESTION_LENGTH
    with pytest.raises(ValueError, match="longer than"):
        clean_question("x" * (MAX_QUESTION_LENGTH + 1))


def test_reads_the_space_id_from_the_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(SPACE_ID_ENV, " 01ef-space ")
    assert space_id_from_env() == "01ef-space"


@pytest.mark.parametrize("value", [None, "", "  "])
def test_missing_space_id_fails_loudly(monkeypatch: pytest.MonkeyPatch, value: str | None) -> None:
    if value is None:
        monkeypatch.delenv(SPACE_ID_ENV, raising=False)
    else:
        monkeypatch.setenv(SPACE_ID_ENV, value)
    with pytest.raises(RuntimeError, match=SPACE_ID_ENV):
        space_id_from_env()


def test_answer_joins_text_and_keeps_the_first_query() -> None:
    reply = message(
        GenieAttachment(text=TextAttachment(content="Sales rose.")),
        GenieAttachment(query=GenieQueryAttachment(description="Monthly sales", query="SELECT 1")),
        GenieAttachment(query=GenieQueryAttachment(query="SELECT 2")),
    )
    assert answer_from_message(reply) == GenieAnswer(
        text="Sales rose.\n\nMonthly sales", sql="SELECT 1", conversation_id="c1"
    )


def test_answer_with_no_attachments_says_so() -> None:
    assert answer_from_message(message()) == GenieAnswer(
        text="Genie returned no text.", sql=None, conversation_id="c1"
    )


def test_answer_surfaces_a_genie_error() -> None:
    answer = answer_from_message(message(error="warehouse stopped"))
    assert answer.text == "Genie reported an error: warehouse stopped"


def test_workspace_genie_asks_its_space() -> None:
    api = FakeGenieAPI(message(GenieAttachment(text=TextAttachment(content="Hi."))))
    workspace = cast(Any, SimpleNamespace(genie=api))
    answer = WorkspaceGenie("s1", workspace=workspace).ask("hello")
    assert api.calls == [("s1", "hello")]
    assert answer.text == "Hi."


def test_workspace_client_is_built_lazily(monkeypatch: pytest.MonkeyPatch) -> None:
    import databricks.sdk

    built: list[object] = []
    api = FakeGenieAPI(message())

    def fake_workspace_client() -> object:
        built.append(api)
        return SimpleNamespace(genie=api)

    monkeypatch.setattr(databricks.sdk, "WorkspaceClient", fake_workspace_client)
    genie = WorkspaceGenie("s1")
    assert built == []
    genie.ask("hello")
    genie.ask("again")
    assert len(built) == 1
    assert api.calls == [("s1", "hello"), ("s1", "again")]
