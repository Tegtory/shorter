from collections.abc import AsyncIterator

from dishka import Provider, Scope, make_async_container
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from shorter.common.config import config
from shorter.domain.interfaces import ILinkRepo
from shorter.domain.use_cases import UCLink
from shorter.infrastructure.repositories.link import SqlAlchemyLinkRepo


def get_engine() -> AsyncEngine:
    return create_async_engine(str(config.database_url))


def get_session_maker(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(engine, expire_on_commit=False)


async def get_session(
    session_maker: async_sessionmaker[AsyncSession],
) -> AsyncIterator[AsyncSession]:
    async with session_maker() as session:
        yield session


provider = Provider()

# Core
provider.provide(get_engine, scope=Scope.APP)
provider.provide(get_session_maker, scope=Scope.APP)
provider.provide(get_session, scope=Scope.REQUEST)

# Repositories
provider.provide(SqlAlchemyLinkRepo, provides=ILinkRepo, scope=Scope.REQUEST)

# Use Cases
provider.provide(UCLink, scope=Scope.REQUEST)


container = make_async_container(provider)
