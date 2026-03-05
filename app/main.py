from app.agent import SupportAgent
from app.models import ChatRequest, ChatResponse
from app.retriever import SimpleRetriever
from app.tools import ToolRegistry

retriever = SimpleRetriever("knowledge_base")
tools = ToolRegistry()
agent = SupportAgent(retriever, tools)


def process_chat(request: ChatRequest) -> ChatResponse:
    if not request.customer_id.strip():
        raise ValueError("customer_id must not be empty")
    if not request.message.strip():
        raise ValueError("message must not be empty")
    return agent.respond(customer_id=request.customer_id, message=request.message)


if __name__ == "__main__":
    sample = ChatRequest(customer_id="cust-123", message="Where is my order ORD-1001?")
    print(process_chat(sample))
