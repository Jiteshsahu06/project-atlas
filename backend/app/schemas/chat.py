
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    client_id: str = Field(min_length=1, max_length=50)
    message: str = Field(min_length=1, max_length=5000)


class ChatResponse(BaseModel):
    answer: str
    category: str
    confidence: float = Field(ge=0, le=1)
    escalation_id: int | None = None
