from dishka import Provider, Scope, make_async_container

from shorter.domain.interfaces import ILinkRepo
from shorter.domain.use_cases import UCLink
from shorter.infrastructure.repositories.link import SQLiteLinkRepo

provider = Provider()
provider.provide(SQLiteLinkRepo, provides=ILinkRepo, scope=Scope.APP)
provider.provide(UCLink, scope=Scope.APP)

container = make_async_container(provider)
