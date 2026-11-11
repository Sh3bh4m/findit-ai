# Laya — decision-model research and controlled routing

**Goal:** Choose a useful information path for each question: exact structured retrieval, semantic retrieval, or language-model response.

The supplied private code supports *different levels of maturity*:

| Stage | Evidence in reviewed source | Public claim |
| --- | --- | --- |
| Intent/rule routing | Query intent parsing and branching in API/schema modules | Implemented routing logic |
| v0.8.x shadow | Records observational decisions; intentionally leaves user-facing routes unchanged | Observational evaluation only |
| v0.9.3 controlled pilot | Activation configuration, eligibility filters, confidence check, narrow read-only project-analysis call and fail-closed fallback | Conditionally available experiment, not general rollout |
| Universal ML-dispatch | No evidence it governs every query across all three paths | Aspirational design, **not claimed as deployed** |

In the public `findit_showcase/decision.py`, a deterministic rule-based selector illustrates Laya's *intended interfaces*; it is not represented as the trained Laya classifier. This separation matters because a strong portfolio should distinguish a production system, an experiment, and a proposed design.

## Safety principles

- For exact counts, prefer verifiable structured data over generated guesses.
- For semantic candidates, revalidate current records before answering.
- Uncertain or unsupported routes must have a transparent fallback.
- An experimental model must be gated, observable, and reversible.
- Do not treat a confidence score alone as proof of answer correctness.

