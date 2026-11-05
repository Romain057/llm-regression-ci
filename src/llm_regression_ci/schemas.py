from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Literal
from datetime import date
import re

Category = Literal["billing", "technical", "account", "general"]

def require_dated_snapshot(v: str) -> str:
    if re.search(r"-\d{4}-\d{2}-\d{2}$", v) is None:
        raise ValueError("pin a dated snapshot, e.g. gpt-6-luna-YYYY-MM-DD")
    else:
        return v

class TicketClassification(BaseModel):
    model_config = ConfigDict(extra="forbid")
    category: Category
    summary: str = Field(min_length=1, max_length=300)


class FewShotExample(BaseModel):
    model_config = ConfigDict(extra="forbid")
    email: str = Field(min_length=1) 
    output: TicketClassification


class PromptConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")
    version: str 
    created_at: date
    description: str
    model: str
    reasoning_effort: Literal["none", "low", "medium", "high"] = "none"
    temperature: float = Field(ge=0, le=1)
    max_completion_tokens: int = Field(gt=0, le=1000)
    system_prompt: str = Field(min_length=1)
    few_shot: list[FewShotExample] = []
    @field_validator("model")
    @classmethod
    def check_model(cls, v: str) -> str:
        return require_dated_snapshot(v)


class ClassificationResult(BaseModel):
    output: TicketClassification | None = None
    raw_output: str | None = None
    error_kind: Literal["invalid_output", "api_error"] | None = None
    error: str | None = None
    latency_ms: float
    input_tokens: int | None = None
    output_tokens: int | None = None

