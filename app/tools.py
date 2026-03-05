from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass
class OrderRecord:
    order_id: str
    status: str
    eta: date | None = None


class ToolRegistry:
    def __init__(self) -> None:
        self.orders: dict[str, OrderRecord] = {
            "ORD-1001": OrderRecord("ORD-1001", "in transit", date(2026, 3, 7)),
            "ORD-1002": OrderRecord("ORD-1002", "delivered", date(2026, 3, 4)),
            "ORD-1003": OrderRecord("ORD-1003", "processing", None),
        }
        self.tickets: list[dict[str, str]] = []

    def lookup_order(self, order_id: str) -> dict[str, str]:
        order = self.orders.get(order_id)
        if not order:
            return {
                "found": "false",
                "message": f"I couldn't find order {order_id}. Please verify the ID.",
            }

        if order.eta:
            return {
                "found": "true",
                "message": f"Order {order.order_id} is {order.status} and expected by {order.eta.isoformat()}.",
            }

        return {
            "found": "true",
            "message": f"Order {order.order_id} is currently {order.status}.",
        }

    def create_ticket(self, customer_id: str, summary: str) -> dict[str, str]:
        ticket_id = f"TKT-{len(self.tickets) + 1:04d}"
        self.tickets.append(
            {
                "ticket_id": ticket_id,
                "customer_id": customer_id,
                "summary": summary,
                "status": "open",
            }
        )
        return {
            "ticket_id": ticket_id,
            "message": f"I've created support ticket {ticket_id}. A human agent will follow up shortly.",
        }
