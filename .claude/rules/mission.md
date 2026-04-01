# Mission Guardrails

## The Mission

ULTRA RELEVANT AND FAST NIST 800-53 chatbot.

## Relevance Rules

- Every RAG change must be validated with `/project:eval` before merging
- Retrieval L2 score for "What is AC-2?" must stay < 1.0
- Answer must cite at least 1 `[p.XX]` reference for NIST control queries
- Control IDs must be bolded: `**AC-2**`, `**AC-2(1)**` — never plain text

## Speed Rules

- P50 latency target: < 2s (measure via `/api/interactions/stats`)
- Any change that adds > 500ms to the median must be justified and approved
- LRU cache must be active for stateless queries in production

## Scope Rules

- DO: improve RAG retrieval, response formatting, streaming, caching
- DO: improve NIST content accuracy, citation quality, agent routing
- DO NOT: add new UI frameworks, reporting features, or non-NIST domains
- DO NOT: add external API integrations beyond Gemini + Render infra
