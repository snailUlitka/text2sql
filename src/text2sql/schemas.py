"""Public request/result contract shared by Python and HTTP callers."""

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class InvokeRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    input: str = Field(min_length=1, max_length=2000)
    top_k: int = Field(default=20, ge=1, le=1000)


class QueryResult(BaseModel):
    sql: str
    columns: list[str]
    rows: list[list[Any]]
    truncated: bool = False


class ExecutionInfo(BaseModel):
    iterations: int
    tool_calls: int
    sql_attempts: int
    sql_errors: int
    corrections: int
    elapsed_seconds: float
    example_ids: list[str]


class InvokeResult(BaseModel):
    answer: str
    sql: str
    result: QueryResult
    execution: ExecutionInfo


class AgentError(Exception):
    """A bounded, credential-free failure suitable for an API response."""

    def __init__(self, code: str, message: str, *, execution: ExecutionInfo | None = None):
        super().__init__(message)
        self.code = code
        self.message = message
        self.execution = execution
