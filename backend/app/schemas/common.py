from pydantic import BaseModel


class Source(BaseModel):
    name: str
    url: str
    icon: str = ""
