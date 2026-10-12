# Small demonstration evaluation

`cases.json` retains the 15 questions from the 2024 project. SQL references run
against the Compose fixture. The first question requires ordered rows; other
questions compare multisets of rows, preserving duplicates and ignoring order.
Column aliases and natural-language phrasing are not scored. This is a small
demonstration check, not an independent benchmark or an answer-quality evaluation.

The old reference for past trips omitted the time predicate; it now uses
`time_in < CURRENT_TIMESTAMP`. The longest-name reference now returns every tie
instead of an arbitrary LIMIT 1. Dates, intervals and numeric values use the same
serialization for reference and model queries. No old expected-answer strings
are used as ground truth.

Each case records semantic overlap with the few-shot collection. `same_intent`
marks the company-list and Washington-plane questions; `related` marks questions
that share entities, filters or joins with examples. This manual annotation is
not a precise measurement of leakage. Results should be read with that overlap
and the three-trip fixture in mind.

After the README quickstart:

```sh
uv run text2sql-eval --reference-only --output /tmp/text2sql-references.json
uv run text2sql-eval --output evals/results.json
```

The second command runs the local LLM sequentially and writes actual SQL,
result rows, timings, selected example IDs and repair counts. Model tags,
available digests, generation parameters and package versions are included.
Initialization and model downloads are excluded from per-question timing;
each question includes retrieval, generation and SQL execution. Progress is
saved after each question. A failed invocation is recorded as a failure, not
as a correct empty result. Read the JSON report before interpreting a score.
