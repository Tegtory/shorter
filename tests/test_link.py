import pytest

from shorter.domain.use_cases.link import UCLink


@pytest.mark.asyncio
async def test_generate_uid() -> None:
    assert await UCLink._generate_uid("deFy") == "deFb"
