import sqlite3

from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import select, func
from shorter.domain import Link
from shorter.domain.interfaces import ILinkRepo
from shorter.infrastructure.repositories.models import LinkModel


class SQLiteLinkRepo(ILinkRepo):
    def __init__(self) -> None:
        self.conn = sqlite3.connect("links.db")
        self.cursor = self.conn.cursor()

        cursor = self.cursor
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS links (
        uid STRING PRIMARY KEY,
        link STRING
        )""")
        self.conn.commit()

    async def create(self, link: Link) -> Link:
        self.cursor.execute(
            """INSERT INTO links (uid, link) VALUES (?, ?)""",
            (link.uid, link.link),
        )
        self.conn.commit()
        return link

    async def get(self, uid: str) -> Link | None:
        self.cursor.execute("SELECT * FROM links WHERE uid = ?", (uid,))
        result = self.cursor.fetchone()

        if not result:
            return None
        return Link(link=result[1], uid=result[0])

    async def get_last(self) -> Link | None:
        self.cursor.execute("SELECT * FROM links ORDER BY rowid DESC LIMIT 1")
        result = self.cursor.fetchone()
        if not result:
            return None
        return Link(link=result[1], uid=result[0])


class SqlAlchemyLinkRepo(ILinkRepo):
    def __init__(self) -> None:
        self.session = AsyncSession()

    async def create(self, link: Link) -> Link:
        model = LinkModel(uid=link.uid, link=link.link)
        self.session.add(model)
        await self.session.commit()
        return link

    async def get(self, uid: str) -> Link | None:
        model = await self.session.get(LinkModel, uid)
        if model:
            return Link(link=model.link, uid=model.uid)
        return None

    async def get_last(self) -> Link | None:
        model = await self.session.get(
            LinkModel,
            await self.session.scalar(select(func.max(LinkModel.id))),
        )
        if model:
            return Link(link=model.link, uid=model.uid)
        return None
