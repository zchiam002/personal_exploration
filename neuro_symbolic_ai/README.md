# Neuro-Symbolic AI — Entry Materials

Deep literature review prepared August 2026, covering the field from 1943 through mid-2026.
Written for a data scientist with strong ML background and no prior NeSy exposure.

## Files

| File | What it is |
|---|---|
| [neurosymbolic_ai_literature_review.md](neurosymbolic_ai_literature_review.md) | **Start here.** History → taxonomies → eight technical families → 2025–26 SOTA → sceptical scorecard → open problems → reading path → runnable tooling |
| [bibliography.md](bibliography.md) | ~150 annotated citations grouped by theme, with verification status and 12 corrected metadata errors |

## If you only have 20 minutes

Read §5 (*The honest scorecard*) of the review first, then §2.4 and §3.7. That gives you the field's
actual empirical standing and the pattern — LLM proposes, symbolic engine verifies — that accounts for
almost all of its 2025–26 activity.

## Method and confidence

Produced by a 13-agent parallel research sweep (~1.2M tokens, 820 tool calls) across foundations, seven
technical sub-areas, a 2025–26 recency sweep, and a deliberately adversarial evidence audit — followed by
two verification passes:

- **Citation audit** — ~75 citations independently adjudicated against the arXiv API, OpenAlex, dblp and
  publisher pages. Result: **zero fabricated papers, zero invented first authors, zero invented venues.**
  Twelve metadata errors found and corrected in place (preprint-vs-journal title drift, page-range
  corruption, one author-name substitution). Several widely-repeated figures turned out to be unsupported
  and were dropped rather than passed on.
- **Completeness critic** — found five structural gaps in the first draft (the Nanjing abductive-learning
  school, the Japanese differentiable-ASP cluster, SATNet and its replication failure, neural algorithmic
  reasoning, ontology/description-logic embeddings) plus several internal contradictions and framing errors.
  All are incorporated.

**Anything that could not be confirmed carries a ⚠ and says why.** Treat those as leads to check, not as
established facts. A handful of 2026 arXiv identifiers surfaced only in search listings and are explicitly
flagged as needing verification before citation.
