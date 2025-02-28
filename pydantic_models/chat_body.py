from pydantic import BaseModel


class ChatBody(BaseModel):
    query: str