from re import findall

from shorter.common.config import config
from shorter.common.exceptions import BlackListError, InvalidURLError
from shorter.domain import Link
from shorter.domain.interfaces import ILinkRepo


class UCLink:
    def __init__(self, repo: ILinkRepo):
        self.repo = repo

    async def create(self, link: Link) -> Link:
        await self.check_blacklist(link.link)
        await self.check_url(link.link)

        last = await self.repo.get_last()
        link.uid = (
            await self._generate_uid(last.uid)
            if last and last.uid
            else await self._generate_uid(config.DIGITS[:3])
        )
        return await self.repo.create(link)

    async def get(self, uid: str) -> str:
        result = await self.repo.get(uid)
        return result.link if result else config.full_path()

    @staticmethod
    async def _generate_uid(last_uid: str) -> str:
        base = len(config.DIGITS)
        num = 0
        for char in last_uid:
            num = num * base + config.DIGITS.index(char)

        num += 1

        if num == 0:
            return config.DIGITS[0]

        new_uid = []
        while num > 0:
            num, remainder = divmod(num, base)
            new_uid.append(config.DIGITS[remainder])

        return "".join(reversed(new_uid))

    async def check_blacklist(self, url: str) -> None:
        for black_url in config.BLACK_LIST:
            if black_url and url.startswith(black_url):
                raise BlackListError

    async def check_url(self, url: str) -> None:
        if not bool(findall(config.URL_TEST, url)):
            raise InvalidURLError
