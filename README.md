# text2sql

A local text-to-SQL agent for a small PostgreSQL database. Ask a question in
English; the agent retrieves similar SQL examples, calls database tools through
Ollama, and returns an answer together with the SQL and bounded result rows.

The project started as an experiment in April–June 2024. The 2026 update provides
an installable Python library and a thin FastAPI v2 service. It is a demonstration
project with a tiny airline fixture, not a production database assistant.

## Quickstart

Requires Python 3.12, [uv](https://docs.astral.sh/uv/), Docker with Compose, and a
running local [Ollama](https://ollama.com/) service. The two models require about
2.8 GB of downloads. Run these commands from the repository root:

```sh
uv sync --locked --group dev
cp .env.example .env
docker compose up -d --wait
ollama pull qwen3:4b-instruct-2507-q4_K_M
ollama pull nomic-embed-text
uv run python examples/invoke.py
```

Compose creates an `airlines` database on `127.0.0.1:5433`. The fixture contains
45 passengers, three companies, three trips and 45 seat assignments. Its dates
are historical and its names and routes are illustrative. The credentials in
Compose and `.env.example` are public local-demo credentials.

The example asks for the first five passenger names in alphabetical order.
The tested model returned `Alice`, `Bob`, `Charlie`, `Christofer`, `David` using
`SELECT DISTINCT passenger_name FROM passenger ORDER BY passenger_name LIMIT 5`.

To stop the demo database, use `docker compose stop`. Initialization SQL runs
when the Compose volume is first created; an existing volume keeps its data.

## Python API

The library can be used without HTTP. Resource construction is explicit:

```python
from langchain_ollama import ChatOllama
from text2sql import Database, SQLAgent, Settings

settings = Settings()
database = Database(settings.database_url.get_secret_value())
database.initialize()
model = ChatOllama(
    model=settings.model,
    base_url=settings.ollama_url,
    temperature=0,
    reasoning=False,
)
agent = SQLAgent(model=model, database=database)
result = agent.invoke("How many passengers are in the database?", top_k=5)
print(result.answer)
print(result.sql)
```

For the configured model, semantic example retrieval and execution limits,
use `build_agent(Settings())` from `text2sql.runtime`, as in
[`examples/invoke.py`](examples/invoke.py). `SQLAgent` also accepts an explicitly
constructed retriever and additional LangChain tools. Module imports do not
connect to a database or instantiate a model.

## HTTP API v2

```sh
uv run uvicorn text2sql.api:app --host 127.0.0.1 --port 8000
```

In another terminal:

```sh
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/text2sql/v2/invoke \
  -H 'Content-Type: application/json' \
  -d '{"input":"How many passengers are in the database?","top_k":5}'
```

The response contains `answer`, `sql`, `result` (column names, rows and a
`truncated` flag), and `execution` (model iterations, tool calls, SQL attempts,
errors, corrections, elapsed time and selected example IDs). Internal model
reasoning and tool-message transcripts are not exposed.

`top_k` is the maximum number of returned rows, including for SQL that omits a
LIMIT. Its default is 20 and the configured maximum is 100. Aggregate queries
still count all matching rows. Validation and bounded-agent failures return
HTTP 422; unavailable model/database/retrieval services return HTTP 503 with
an `error.code` and a short message. FastAPI's `/docs` shows the schemas.

The service loads resources during startup. `/health` confirms startup
readiness; it does not probe dependencies on every request. API v1 is removed.
The Python package version (0.2.0) is separate from the HTTP API version.

## How it works

- LangChain's `ChatOllama` binds native tools. One bounded loop dispatches
  validated calls and sends observations back as tool messages.
- An in-memory semantic index selects three of 18 SQL examples using
  `nomic-embed-text`; it requires no pgvector service.
- PostgreSQL errors return to the same model loop for correction. Defaults
  allow eight model calls and 16 tool calls per question.
- Database queries use a separate SELECT-only login, a three-second statement
  timeout, an enforced row limit and a 20,000-character serialized-result cap.

Configuration comes from `TEXT2SQL_*` environment variables or `.env`;
see [`.env.example`](.env.example). uv separates runtime dependencies from
development tools. There is no direct LangServe or LangSmith integration;
`langsmith` is currently a transitive dependency of LangChain Core.

## Checks and evaluation

```sh
uv run ruff check .
uv run ruff format --check .
uv run pytest -m "not db"
TEXT2SQL_TEST_DATABASE_URL=postgresql://text2sql_reader:demo_reader@127.0.0.1:5433/airlines \
  uv run pytest -m db
uv run text2sql-eval --reference-only --output /tmp/text2sql-references.json
uv run text2sql-eval --output evals/results.json
```

CI runs Ruff and fast tests with a scripted model, without an LLM or database.
The DB smoke test and real LLM evaluation are separate manual checks.
The [15-question evaluation](evals/README.md) compares SQL result rows rather
than answer wording. Some questions overlap semantically with few-shot examples,
and the database has only three trips. A score on this set is a demonstration
result, not a general accuracy claim.

On 2026-10-08, `qwen3:4b-instruct-2507-q4_K_M` with `nomic-embed-text` matched
all 15 reference SQL results, with a median of 3.969 seconds per question and
one SQL correction. The run used Python 3.12.11, PostgreSQL 17.11 and a 16 GB
ARM64 Mac. [The recorded results](evals/results.json) include model digests,
generation parameters and the actual SQL. Natural-language answers were not scored.

## Limits

Small local models can generate incorrect SQL, stop before calling a tool, or
misstate a correct database result. SQL-row equality does not score the final
answer's factual quality. A successful query is evidence, not a guarantee that
the agent interpreted the question correctly.

The prompt and SQL parser are not a security sandbox. SELECT may call database
functions; use a dedicated account and restrict schemas, roles, functions and
data when adapting this demo. An individual large value can be transferred
before the character cap is checked. The HTTP service has no authentication
and is intended to run locally. See [design notes](docs/design.md) for the
database boundary and migration decisions.

## License

[MIT](LICENSE). Model weights and dependencies have their own licenses.

[Historical approach (2024)](docs/design.md)
