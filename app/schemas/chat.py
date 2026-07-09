from pydantic import BaseModel, Field

class ChatMessage(BaseModel):
    role: str = Field(..., description="The role of the message author (user or assistant)")
    content: str = Field(..., description="The content of the message")

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000, description="The text input sent by the user")
    # You can naturally expand this model to include config metrics like temperature or user_id