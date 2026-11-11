# Semantic retrieval and provenance

The examined semantic track integrates FileMaker text records with an opt-in index. It includes embedding generation, vector comparison, selected collection scopes, and current-record verification.

## Key decisions

1. **Limit scope.** Only selected collections and fields are candidates; indexes should not cross tenant or user authorization boundaries.
2. **Compute embeddings.** The private project includes an EmbeddingGemma track using 768-dimensional vectors. This public example intentionally has no model weights or private text.
3. **Rank candidates.** Use cosine similarity to identify promising records, then optionally apply lexical signals or business-specific constraints.
4. **Verify freshness.** Compare the indexed content's hash to a freshly retrieved authorized record before using a candidate as evidence.
5. **Fail safely.** Missing, modified, or unauthorized records are dropped from retrieval results; a weak match must not be presented as a certain answer.

`findit_showcase/semantic.py` demonstrates steps 3 and 4 with *synthetic vectors*. It is deliberately small and independent of FileMaker infrastructure. It should not be benchmarked as if it used the private EmbeddingGemma model.

## Deployment maturity

The reviewed source supports a restricted live semantic bridge for selected tasks/story collections. Broader knowledge and epic indexing and combined-query changes appear in staged artifacts; their production rollout is not verified from source files alone.

