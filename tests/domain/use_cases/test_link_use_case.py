import pytest

from shorter.common.config import config
from shorter.domain import Link
from shorter.domain.interfaces import ILinkRepo
from shorter.domain.use_cases.link import UCLink


class MockLinkRepo(ILinkRepo):
    def __init__(self) -> None:
        self._links: list[Link] = []

    async def create(self, link: Link) -> Link:
        self._links.append(link)
        return link

    async def get(self, uid: str) -> Link | None:
        for link in self._links:
            if link.uid == uid:
                return link
        return None

    async def get_last(self) -> Link | None:
        if not self._links:
            return None
        return self._links[-1]


@pytest.fixture
def mock_repo() -> MockLinkRepo:
    return MockLinkRepo()


@pytest.fixture
def link_use_case(mock_repo: MockLinkRepo) -> UCLink:
    return UCLink(repo=mock_repo)


@pytest.mark.asyncio
async def test_generate_uid() -> None:
    assert await UCLink._generate_uid("0") == "1"
    assert await UCLink._generate_uid("9") == "a"
    assert await UCLink._generate_uid("Z") == "10"
    assert await UCLink._generate_uid("10") == "11"


@pytest.mark.asyncio
async def test_get_existing_link(
    link_use_case: UCLink, mock_repo: MockLinkRepo
) -> None:
    link = Link(link="https://example.com", uid="a")
    await mock_repo.create(link)

    result = await link_use_case.get("a")
    assert result == "https://example.com"


@pytest.mark.asyncio
async def test_get_non_existing_link(link_use_case: UCLink) -> None:
    result = await link_use_case.get("nonexistent")
    assert result == config.full_path()
