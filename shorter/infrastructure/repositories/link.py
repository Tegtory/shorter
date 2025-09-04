from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from shorter.domain import Link
from shorter.domain.interfaces import ILinkRepo
from shorter.infrastructure.repositories.models import LinkModel


class SqlAlchemyLinkRepo(ILinkRepo):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, link: Link) -> Link:
        model = LinkModel(uid=link.uid, link=link.link)
        self.session.add(model)
        await self.session.flush()
        await self.session.refresh(model)
        return link

    async def get(self, uid: str) -> Link | None:
        stmt = select(LinkModel).where(LinkModel.uid == uid)
        model = await self.session.scalar(stmt)
        if model:
            return Link(link=model.link, uid=model.uid)
        return None

    async def get_last(self) -> Link | None:
        stmt = select(LinkModel).order_by(LinkModel.id.desc())
        model = (await self.session.execute(stmt)).scalars().first()
        if model:
            return Link(link=model.link, uid=model.uid)
        return None
