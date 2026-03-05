from dataclasses import dataclass


@dataclass
class ChatRequest:
    customer_id: str
    message: str


@dataclass
class ChatResponse:
    reply: str
    action: str
    confidence: float
    escalate: bool
    sources: list[str]
