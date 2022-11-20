from pydantic import BaseModel, Field
from typing import Optional


class User(BaseModel):
    id: int
    first_name: str
    username: str


class Chat(BaseModel):
    id: int


class Message(BaseModel):
    message_id: int
    from_: User = Field(..., alias='from')
    chat: Chat
    text: Optional[str] = None


class ModelMessage(BaseModel):
    update_id: int
    message: Message
