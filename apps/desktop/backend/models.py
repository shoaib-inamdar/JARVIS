from pydantic import BaseModel


class ChatRequest(BaseModel):
    """Defines what the /chat endpoint expects to receive."""

    message: str
    session_id: str = "default"  # optional — defaults to "default"


class ChatResponse(BaseModel):
    """Defines what the /chat endpoint sends back."""

    reply: str
    message_count: int
    status: str


class HealthResponse(BaseModel):
    """What /health sends back."""

    status: str
    version: str
    agent_ready: bool


class CodingRequest(BaseModel):
    message: str
    project_root: str = "."
    open_file: str = ""
    error_context: str = ""
