from pydantic import BaseModel


class Link(BaseModel):
    link: str
    uid: str | None = None
