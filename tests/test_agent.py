from app.main import process_chat
from app.models import ChatRequest


def test_order_lookup_success() -> None:
    payload = process_chat(ChatRequest(customer_id="cust-1", message="Can you check order ORD-1001?"))
    assert payload.action == "order_status"
    assert payload.escalate is False
    assert "ORD-1001" in payload.reply


def test_asks_for_order_id_when_missing() -> None:
    payload = process_chat(ChatRequest(customer_id="cust-2", message="Where is my order?"))
    assert payload.action == "ask_order_id"
    assert "Please share your order ID" in payload.reply


def test_faq_retrieval_path() -> None:
    payload = process_chat(ChatRequest(customer_id="cust-3", message="What is your returns policy?"))
    assert payload.action == "faq"
    assert payload.sources


def test_risky_request_triggers_escalation() -> None:
    payload = process_chat(ChatRequest(customer_id="cust-4", message="I need a refund now"))
    assert payload.escalate is True
