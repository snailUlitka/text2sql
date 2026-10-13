# text2sql

A local agent that turns English questions into PostgreSQL queries and answers,
returning SQL, rows and execution metadata. Uses Ollama and LangChain through a
Python library and thin FastAPI v2 service.

Started in April–June 2024; rebuilt as an installable package in 2026. This is a
demonstration project using a small airline database.

## Question → SQL → answer

> Print the first 5 names of the passengers, sorted by name

```sql
SELECT DISTINCT "passenger_name" FROM "passenger"
ORDER BY "passenger_name" LIMIT 5
```

**Answer:** Alice, Bob, Charlie, Christofer, David.

## Quickstart

Requires Python 3.12, [uv](https://docs.astral.sh/uv/), Docker Compose and a running
local [Ollama](https://ollama.com/) service. Models require about 2.8 GB of downloads.
From the repository root:

```sh
uv sync --locked --group dev
cp .env.example .env
docker compose up -d --wait
ollama pull qwen3:4b-instruct-2507-q4_K_M
ollama pull nomic-embed-text
uv run --locked python examples/invoke.py
```

The demo on `127.0.0.1:5433` contains 45 passengers, three companies and three trips.
[`.env.example`](.env.example) contains public demo credentials.
`docker compose stop` stops the database and retains its data.

## Recorded evaluation

**15/15 SQL-result matches on a small demonstration set**, recorded on 2026-10-08.
The evaluation compares query result rows with reference SQL results; row order
matters only where specified.

| Model | Embeddings | Median per question | SQL corrections |
| --- | --- | --- | --- |
| `qwen3:4b-instruct-2507-q4_K_M` | `nomic-embed-text` | 3.969 s | 1 |

Run settings: temperature 0, seed 42, context 8192, output limit 1024 tokens,
reasoning disabled.
[Recorded SQL, rows and model digests](evals/results.json) ·
[Evaluation method and commands](evals/README.md).

Questions partly overlap with few-shot examples. This is not a general accuracy
estimate; natural-language answer quality was not scored.

## Engineering decisions

- **Explicit resources:** imports have no database/model side effects; FastAPI
  initializes resources at startup. Configuration uses `TEXT2SQL_*` or `.env`.
- **Native tool calling:** validated LangChain/Ollama calls and SQL repair share
  one loop, capped at eight model calls and 16 tool calls per question.
- **Few-shot retrieval:** an in-memory semantic index selects three of 18 SQL
  examples, without a separate vector database.
- **Bounded database access:** a dedicated SELECT-only login, three-second
  statement timeout, enforced row limit and 20,000-character serialized-result cap.
- **Reproducibility:** uv.lock and a seven-day release cooldown; CI runs Ruff and
  scripted-model tests without an LLM or database.

See [design notes](docs/design.md) for tradeoffs and migration decisions, including
removal of direct LangServe/LangSmith integrations.

## Development checks

```sh
uv run --locked ruff check .
uv run --locked ruff format --check .
uv run --locked pytest -m "not db"
```

The optional database smoke test requires the running Compose demo:

```sh
TEXT2SQL_TEST_DATABASE_URL=postgresql://text2sql_reader:demo_reader@127.0.0.1:5433/airlines \
  uv run --locked pytest -m db
```

## API reference

### Python

The configured factory enables retrieval and execution limits:

```python
from text2sql import Settings
from text2sql.runtime import build_agent

agent = build_agent(Settings())
result = agent.invoke("How many passengers are in the database?", top_k=5)
print(result.answer)
print(result.sql)
```

`SQLAgent` also accepts an explicit model, `Database`, retriever and extra tools.
See [the runnable example](examples/invoke.py).

### HTTP v2

```sh
uv run --locked uvicorn text2sql.api:app --host 127.0.0.1 --port 8000
```

In another terminal:

```sh
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/text2sql/v2/invoke \
  -H 'Content-Type: application/json' \
  -d '{"input":"How many passengers are in the database?","top_k":5}'
```

Responses contain `answer`, `sql`, `result` (columns, rows, `truncated`) and
`execution` (iterations, tool calls, SQL attempts/errors/corrections, timing and
example IDs). Internal reasoning is not exposed.

`top_k` caps returned rows even without LIMIT (default 20, maximum 100); aggregates
still count all matching rows. Validation and agent-limit failures return HTTP 422;
unavailable dependencies return HTTP 503 with `error.code` and a message.
`/docs` provides full schemas; `/health` reports startup readiness.

## Limitations

Models can generate incorrect SQL or misstate results. The prompt/parser are not
a sandbox: restrict database privileges when adapting the demo. Large values may
be transferred before the character cap is checked. HTTP has no authentication
and is intended for local use.

[MIT license](LICENSE). Models and dependencies have their own licenses.

[Historical approach (2024)](docs/design.md)
