from __future__ import annotations

import re

from app.models import ChatResponse
from app.retriever import SimpleRetriever
from app.tools import ToolRegistry


class SupportAgent:
    ORDER_REGEX = re.compile(r"\bORD-\d{4}\b", re.IGNORECASE)

    def __init__(self, retriever: SimpleRetriever, tools: ToolRegistry) -> None:
        self.retriever = retriever
        self.tools = tools

    def _needs_escalation(self, message: str, confidence: float) -> bool:
        high_risk_keywords = ["refund", "chargeback", "password", "account delete", "legal"]
        lowered = message.lower()
        if any(word in lowered for word in high_risk_keywords):
            return True
        return confidence < 0.45

    def respond(self, customer_id: str, message: str) -> ChatResponse:
        lowered = message.lower()

        if "order" in lowered:
            match = self.ORDER_REGEX.search(message)
            if match:
                data = self.tools.lookup_order(match.group(0).upper())
                confidence = 0.96 if data["found"] == "true" else 0.75
                escalate = self._needs_escalation(message, confidence)
                return ChatResponse(
                    reply=data["message"],
                    action="order_status",
                    confidence=confidence,
                    escalate=escalate,
                    sources=[],
                )

            return ChatResponse(
                reply="I can check that for you. Please share your order ID (for example, ORD-1001).",
                action="ask_order_id",
                confidence=0.8,
                escalate=False,
                sources=[],
            )

        if "human" in lowered or "agent" in lowered or "escalate" in lowered:
            ticket = self.tools.create_ticket(customer_id, message)
            return ChatResponse(
                reply=ticket["message"],
                action="escalate",
                confidence=0.99,
                escalate=True,
                sources=[],
            )

        chunks = self.retriever.search(message)
        if chunks:
            top = chunks[0]
            reply = (
                "Based on our policy: "
                + top.content.splitlines()[0].replace("#", "").strip()
                + ". If you want, I can connect you to a human agent."
            )
            confidence = min(0.9, max(0.45, top.score + 0.2))
            escalate = self._needs_escalation(message, confidence)
            return ChatResponse(
                reply=reply,
                action="faq",
                confidence=round(confidence, 2),
                escalate=escalate,
                sources=[chunk.source for chunk in chunks],
            )

        ticket = self.tools.create_ticket(customer_id, f"Unhandled question: {message}")
        return ChatResponse(
            reply=(
                "I want to make sure you get an accurate answer. "
                + ticket["message"]
            ),
            action="fallback_escalation",
            confidence=0.3,
            escalate=True,
            sources=[],
        )
