---
name: nist-focus
description: Mission drift detector — triggers when task contains scope-creep keywords
triggers:
  - "add feature"
  - "new page"
  - "UI change"
  - "dashboard"
  - "report generator"
  - "new framework"
  - "integrate with"
---

# NIST Focus Skill — Mission Alignment Check

## This Skill Triggered Because

The task description contains words associated with scope creep. Before proceeding, verify mission alignment.

## Mission Alignment Test

Ask yourself:

1. **Does this change improve NIST 800-53 retrieval accuracy?**
   - Yes → proceed
   - No → see below

2. **Does this change reduce response latency?**
   - Yes → proceed
   - No → see below

3. **Does this change improve citation correctness or answer quality?**
   - Yes → proceed
   - No → STOP

## If the answer is "No" to all three:

The proposed change is **out of scope** for v03. Defer it or get explicit user confirmation that it serves the mission.

## Scope Reminder

| IN SCOPE | OUT OF SCOPE |
|----------|-------------|
| RAG retrieval improvements | New UI pages or frameworks |
| Response formatting (citations, bold IDs) | Report generation features |
| Caching and latency optimization | Non-NIST compliance domains |
| Streaming endpoint | External API integrations (non-Gemini) |
| Interaction logging and stats | Analytics dashboards |
| NIST 800-53 content accuracy | Multi-tenant features |

## Escalation

If the user explicitly asks for an out-of-scope feature, acknowledge the request, explain the scope constraint, and ask for explicit confirmation before proceeding.
