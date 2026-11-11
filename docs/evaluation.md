# Reproducibility and evaluation

## Included, runnable evidence

```bash
python3 -m unittest discover -s tests -v
python3 -m examples.demo
```

Tests verify routing precedence, parameterized exact counting, query isolation, vector ranking, and exclusion of stale or out-of-scope records. All fixtures are fabricated.

## Recommended future evaluation (not claimed as complete)

- **Routing:** Label a held-out set of queries and measure per-class precision/recall, ambiguity and fallback rates.
- **Exact answers:** Compare structured answers to manually validated FileMaker results.
- **Semantic:** Precision@k, MRR, freshness checks and record-level access controls.
- **Safety:** Prompt-injection boundaries, read/write authorization, secret scanning and deployment rollback.
- **Performance:** p50/p95 latency and failure rate across realistic query categories.

No private customer results, accuracy percentages or latency numbers are asserted here without reproducible evidence.

