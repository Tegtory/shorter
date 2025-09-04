from unittest.mock import MagicMock

import pytest
from dishka import Provider, Scope, make_async_container, provide
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI, status
from fastapi.testclient import TestClient

from shorter.domain import Link
from shorter.domain.interfaces import ILinkRepo
from shorter.domain.use_cases.link import UCLink
from shorter.presentors.fastapi.handlers import router


class MockUCLink(UCLink):
    async def create(self, link: Link) -> Link:
        link.uid = "testuid"
        return link

    async def get(self, uid: str) -> str:
        if uid == "testuid":
            return "https://example.com"
        return "http://127.0.0.1"


class MockProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_use_case(self) -> UCLink:
        return MockUCLink(repo=MagicMock(spec=ILinkRepo))


@pytest.fixture
def app() -> FastAPI:
    app = FastAPI()
    app.include_router(router)
    container = make_async_container(MockProvider())
    setup_dishka(container, app)
    return app


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    return TestClient(app)


def test_create_url(client: TestClient) -> None:
    response = client.post("/gen", json={"link": "https://example.com"})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"link": "https://example.com", "uid": "testuid"}


def test_get_url(client: TestClient) -> None:
    response = client.get("/testuid", follow_redirects=False)
    assert response.status_code == status.HTTP_302_FOUND
    assert (
        '<script>window.location.href="https://example.com"</script>'
        in response.text
    )


def test_get_url_not_found(client: TestClient) -> None:
    response = client.get("/nonexistent", follow_redirects=False)
    assert response.status_code == status.HTTP_302_FOUND
    assert (
        '<script>window.location.href="http://127.0.0.1"</script>'
        in response.text
    )
