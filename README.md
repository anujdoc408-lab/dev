# Customer Service AI Agent Starter

A production-minded starter kit for a **customer service AI agent** that can:

- Answer FAQ questions with retrieval over local policy docs.
- Check order status via a tool.
- Create support tickets via a tool.
- Escalate to a human when confidence is low or sensitive requests occur.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest
```

Run a sample interaction:

```bash
python -m app.main
```

## What this implementation includes

- `SimpleRetriever`: lightweight keyword-overlap retrieval over markdown docs in `knowledge_base/`.
- `ToolRegistry`: in-memory tools for order lookup and ticket creation.
- `SupportAgent`: orchestration with intent detection, retrieval fallback, and policy guardrails.
- `Guardrails`: automatically escalates for high-risk intents (refunds/account changes/password)
  or low-confidence responses.

## Core files

- `app/agent.py` – routing, intent handling, guardrails, final response builder.
- `app/retriever.py` – local knowledge base retrieval.
- `app/tools.py` – order lookup + ticket creation tool implementations.
- `app/main.py` – `process_chat(...)` entry point.
- `tests/test_agent.py` – basic behavior tests.

## Next steps for production

- Replace in-memory DB with your real CRM/order backend.
- Expose `process_chat` with FastAPI/Flask if you need HTTP.
- Add authentication and role-based permissions.
- Add conversation memory and user profile context.
- Add observability (trace IDs, latency, CSAT outcomes).
- Add human handoff integration (Zendesk/Intercom/Freshdesk).
