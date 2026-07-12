from typing import Optional

from pydantic import BaseModel, Field


class UserInfo(BaseModel):
    sub: str
    email: Optional[str] = None
    name: Optional[str] = None
    picture: Optional[str] = None


class ChatMessage(BaseModel):
    role: str = Field(
        ...,
        description="The role of the message author (user or assistant)"
    )
    content: str = Field(
        ...,
        description="The content of the message"
    )


class ChatRequest(BaseModel):
    message: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="The text input sent by the user"
    )

    user: UserInfo