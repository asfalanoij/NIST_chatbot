# API Conventions

## Stable Response Schema (NEVER change these keys)

```json
{
  "answer": "string",
  "sources": [{"source": "...", "page": 0, "snippet": "..."}],
  "agent_name": "string",
  "agent_id": "string"
}
```

New optional keys may be added (e.g., `word_count`, `cached`, `latency_ms`) but existing keys must not be renamed or removed.

## Rate Limits

- `/api/chat`: 10 requests/minute per IP
- `/api/ingest`: 5 requests/minute per IP (disabled in prod via `DISABLE_INGEST=true`)
- `/api/interactions/stats`: 60 requests/minute (admin only)

## Authentication

- `@require_api_key` decorator on all endpoints
- Empty `API_KEY` env var = dev mode (no auth required)
- Pass key via `X-Api-Key` header or `Authorization: Bearer <key>`

## SSE Conventions (Phase 4)

- Endpoint: `POST /api/chat/stream`
- Content-Type: `text/event-stream`
- Header: `X-Accel-Buffering: no`
- Event sequence:
  1. `{"type": "meta", "agent_name": "...", "agent_id": "..."}`
  2. `{"chunk": "..."}` × N (token chunks)
  3. `[DONE]`
- Interaction logging fires AFTER stream completes (buffered)

## Error Responses

```json
{"error": "human-readable message", "code": "SNAKE_CASE_CODE"}
```

Never expose stack traces or internal paths in error responses.
