from sqlalchemy import BigInteger, String
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True


class LinkModel(Base):
    __tablename__ = "links"

    id: Mapped[str] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True
    )
    uid: Mapped[str] = mapped_column(String)
    link: Mapped[str]
