# Design and historical approach

## The 2024 implementation

The project explored local models for querying a small PostgreSQL airline database
between April and June 2024. Early experiments used retrieved examples to produce
SQL; the final version used LangChain's experimental `OllamaFunctions` wrapper.

The cleaned historical snapshot includes the
[agent](https://github.com/snailUlitka/text2sql/blob/2903d9c8f09375d947d0fe9822ff123b9a6e6f50/app/llm_app/agents/ollama_functions_agent.py),
[query tool and human-message observations](https://github.com/snailUlitka/text2sql/blob/2903d9c8f09375d947d0fe9822ff123b9a6e6f50/app/llm_app/tools/sql_query_tool.py),
and [example notebook](https://github.com/snailUlitka/text2sql/blob/2903d9c8f09375d947d0fe9822ff123b9a6e6f50/examples/sql_agent.ipynb).

That wrapper asked the model to emit a JSON representation of a function call and
passed it through an OpenAI functions parser. The application dispatched custom
tools for table discovery, schema inspection, SQL checking and query execution.
Tool observations were then rephrased as human messages, with instructions to fix
an incorrect query or produce an answer. These messages were a compatibility
workaround, rather than native tool responses.

Similar questions were selected with embeddings and PGVector. The checker made
another model call to review SQL before execution. A bounded agent loop kept the
intermediate tool actions. FastAPI exposed a v1 invocation route; the server also
constructed a LangSmith client. Dependencies included LangServe.

This implementation had practical problems: the endpoint ignored `top_k`, extra
tools were not appended, string tool inputs were dispatched incorrectly,
configuration imports disagreed with the generated file location, and test data
executed SQL during import. Windows paths and a frozen environment-wide dependency
list made setup difficult. A single `SET ROLE` was not a reliable way to constrain
all database connections.

Historical experiment files do not establish reproducible accuracy figures: some
few-shot JOINs were invalid, expected answer strings contained mistakes, and the
evaluation questions overlapped with examples. The 2026 evaluation compares SQL
rows instead of relying on those answer strings.

## The 2026 implementation

The installed `text2sql` package contains one `SQLAgent` loop. It uses LangChain
messages and tools with `ChatOllama.bind_tools()`. Native `AIMessage.tool_calls`
are validated and dispatched, and observations return as `ToolMessage` objects
with the matching call ID. A SQL error goes back through that same loop; there
is no separate retry agent or SQL-checker model. Model and tool-call budgets
also bound repeated errors and schema calls.

The Python caller supplies the database, chat model and optional example
retriever. `Database.initialize()` inspects a supplied database explicitly.
`build_agent(Settings())` provides a convenience factory. No module creates a
connection or model at import time. Each invocation keeps its conversation and
execution counters locally, so the HTTP endpoint uses the same library code.

The example index uses `SemanticSimilarityExampleSelector` with an
`InMemoryVectorStore` and Ollama embeddings. Eighteen examples do not justify
a second persistent database; startup computes their vectors, then each question
selects three similar examples. `top_k` controls database result rows and is
independent of the retrieval count. Some examples legitimately return no rows
on this tiny fixture.

FastAPI initializes resources in lifespan and exposes only API v2. Requests accept
`input` and `top_k`; results include the answer, SQL, bounded result rows and
execution counts. Raw model messages and reasoning are not included. HTTP API v2
and Python package version 0.2.0 are independent version numbers.

## Database boundary and limits

The demo connects as `text2sql_reader`, which has SELECT privileges on the four
public tables and owns none of them. Startup rejects privileged logins and
public-table write privileges. Each fresh connection applies a statement timeout
and read-only transaction setting. A PostgreSQL SQL parser rejects multiple
statements, modifying statements, modifying CTEs, SELECT INTO and locking clauses.
An outer LIMIT and a bounded fetch enforce the requested row limit; an extra row
detects truncation. Oversized serialized results are rejected at 20,000 characters.

The database grants are the durable write boundary. The SQL parser and prompt
are additional checks, not a general SQL security sandbox. SELECT can call
functions; a different database must restrict accessible schemas, functions,
roles and data appropriately. Row and character caps do not prevent an individual
large PostgreSQL value from being transferred before the size check. This demo
is intended for local use, has no authentication, and is not a production data
access gateway. `/health` reports startup readiness, not a live dependency probe.

There is no direct LangSmith or LangServe client, dependency declaration, or
tracing configuration. LangChain Core currently depends on `langsmith`
transitively; its presence in the lockfile does not mean this project uses the
hosted tracing service. Users should not externally enable LangChain tracing
when they want model and database data to remain local.

## Fixture provenance

The four-table fixture and question list were already present in the repository
in 2024. They use a small list of common names, airline names, illustrative seats
and three flights, rather than an imported passenger dataset. The modern SQL keeps
those values, including historical spellings such as `Poul`, `Christofer`, `Tokio`
and `Gongkong`, and converts dates to unambiguous ISO literals. Git history records
contributions under the author's Snail/snailUlitka identities. No third-party data
source or dataset license was recorded in the original files. Do not interpret
the fixture as real passenger information or actual airline schedules.

The current tree replaces notebooks and opaque experiment pickles with a Python
example, readable question definitions and a reproducible manual evaluation
report. Historical code remains in the cleaned Git history. Modern changes carry
their actual 2026 dates.

## Integration references

- [LangChain ChatOllama and native tool calls](https://docs.langchain.com/oss/python/integrations/chat/ollama)
- [LangChain in-memory vector store](https://docs.langchain.com/oss/python/integrations/vectorstores/in_memory)
- [PostgreSQL privileges](https://www.postgresql.org/docs/17/sql-grant.html)
- [Ollama Qwen3 Instruct](https://ollama.com/library/qwen3:4b-instruct-2507-q4_K_M)
