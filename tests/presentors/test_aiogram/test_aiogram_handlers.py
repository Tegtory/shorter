from unittest.mock import AsyncMock, MagicMock

import pytest
from dishka import Provider, Scope, make_async_container, provide

from shorter.domain import Link
from shorter.domain.interfaces import ILinkRepo
from shorter.domain.use_cases.link import UCLink
from shorter.presentors.aiogram.handlers import create_url, start
from shorter.presentors.aiogram.messages import welcome


class MockUCLink(UCLink):
    async def create(self, link: Link) -> Link:
        link.uid = "testuid"
        return link


@pytest.mark.asyncio
async def test_start_handler() -> None:
    message = MagicMock()
    message.answer = AsyncMock()

    await start(message)

    message.answer.assert_called_once_with(welcome)


@pytest.mark.asyncio
async def test_create_url_handler() -> None:
    message = MagicMock()
    message.answer = AsyncMock()
    message.text = "https://example.com"

    class MockProvider(Provider):
        @provide(scope=Scope.APP)
        def get_use_case(self) -> UCLink:
            return MockUCLink(repo=MagicMock(spec=ILinkRepo))

    container = make_async_container(MockProvider())

    await create_url(message=message, dishka_container=container)

    message.answer.assert_called_once()
    call_args = message.answer.call_args[0][0]
    assert "testuid" in call_args
    await container.close()
