# /project:eval — RAG Quality Evaluation

Run the RAG evaluator and print interaction stats. Use after any retrieval change.

## Test Queries

The eval runs these 5 canonical queries and checks:
- L2 relevance score < 1.0
- At least 1 `[p.XX]` citation in answer
- Answer ≤ 200 words
- Control IDs bolded `**AC-2**`

```
1. "What is AC-2?"
2. "Describe the requirements for IA-5 authenticator management."
3. "What controls apply to access control for mobile devices?"
4. "What is SC-28 and when is it required?"
5. "What is the difference between AC-2 and AC-3?"
```

## Running the Eval

```bash
make eval
```

Or manually:
```bash
cd backend
./venv/bin/python -c "
from rag_engine import RAGEngine
engine = RAGEngine()
queries = [
    'What is AC-2?',
    'Describe IA-5 requirements.',
    'Access control for mobile devices.',
    'What is SC-28?',
    'Difference between AC-2 and AC-3?'
]
for q in queries:
    result = engine.chat(q, [], 'NIST_SPECIALIST')
    print(f'Q: {q}')
    print(f'  sources: {len(result[\"sources\"])} | words: {len(result[\"answer\"].split())}')
"
```

## Interpreting Results

- avg_relevance_score < 1.0: retrieval is on-target
- avg_word_count < 180: answers are concise
- avg_citation_count > 1: citations present
- cache_hit_rate > 0.3: cache is warming up
