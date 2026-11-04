from pydantic import BaseModel
from typing import Literal
from datetime import date

Category = Literal["billing", "technical", "account", "general"]

class TicketClassification(BaseModel):
    category: Category
    summary: str


class FewShotExample(BaseModel):
    email: str
    output: TicketClassification


class PromptConfig(BaseModel):
    version: str 
    created_at: date
    description: str
    model: str
    reasoning_effort: Literal["billing", "technical", "account", "general"]
    temperature: float
    max_completion_tokens: int
    system_prompt: str
    few_shot: list[FewShotExample]


class ClassificationResult(BaseModel):
    output: TicketClassification | None = None
    raw_output: str | None = None
    error_kind: Literal["invalid_output", "api_error"] | None = None
    error: str | None = None
    latency_ms: float
    input_token: int | None = None
    output_token: int | None = None