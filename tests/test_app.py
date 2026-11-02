from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from app.backend.main import app, genie
from genie_app_workshop import GenieAnswer, WorkspaceGenie


class FakeGenie:
    def __init__(self) -> None:
        self.questions: list[str] = []

    def ask(self, question: str) -> GenieAnswer:
        self.questions.append(question)
        return GenieAnswer(text="Sales rose.", sql="SELECT 1", conversation_id="c1")


@pytest.fixture
def fake() -> Iterator[FakeGenie]:
    fake = FakeGenie()
    app.dependency_overrides[genie] = lambda: fake
    yield fake
    app.dependency_overrides.clear()


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def test_health(client: TestClient) -> None:
    assert client.get("/api/health").json() == {"status": "ok"}


def test_ask_returns_genies_answer(client: TestClient, fake: FakeGenie) -> None:
    res = client.post("/api/genie/ask", json={"question": " top products? "})
    assert res.status_code == 200
    assert res.json() == {"text": "Sales rose.", "sql": "SELECT 1", "conversation_id": "c1"}
    assert fake.questions == ["top products?"]


def test_blank_question_is_422(client: TestClient, fake: FakeGenie) -> None:
    res = client.post("/api/genie/ask", json={"question": "  "})
    assert res.status_code == 422
    assert res.json() == {"detail": "question is required"}
    assert fake.questions == []


def test_missing_question_field_is_422(client: TestClient, fake: FakeGenie) -> None:
    assert client.post("/api/genie/ask", json={}).status_code == 422


def test_serves_the_page(client: TestClient) -> None:
    res = client.get("/")
    assert res.status_code == 200
    assert "Ask Genie" in res.text


def test_real_dependency_targets_the_configured_space(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("GENIE_SPACE_ID", "s1")
    genie.cache_clear()
    try:
        client = genie()
        assert isinstance(client, WorkspaceGenie)
        assert client.space_id == "s1"
    finally:
        genie.cache_clear()
