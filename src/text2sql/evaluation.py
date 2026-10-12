"""Manual 15-question demonstration evaluation, comparing SQL result rows."""

import argparse
import datetime as dt
import json
import platform
import statistics
from collections import Counter
from importlib.metadata import version
from pathlib import Path
from time import perf_counter
from urllib.request import urlopen

from text2sql.config import Settings
from text2sql.database import Database
from text2sql.runtime import build_agent
from text2sql.schemas import AgentError


def same_rows(expected: list[list], actual: list[list], *, ordered: bool) -> bool:
    if ordered:
        return expected == actual

    def encode(row):
        return json.dumps(row, sort_keys=True, default=str)

    return Counter(map(encode, expected)) == Counter(map(encode, actual))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cases", type=Path, default=Path("evals/cases.json"))
    parser.add_argument("--output", type=Path, default=Path("evals/results.json"))
    parser.add_argument("--reference-only", action="store_true", help="Validate SQL without an LLM")
    args = parser.parse_args()
    settings = Settings()
    cases = json.loads(args.cases.read_text())
    if args.reference_only:
        db = Database(settings.database_url.get_secret_value(), max_rows=settings.max_rows)
        db.initialize()
        agent = None
    else:
        agent = build_agent(settings)
        db = agent.database
    metadata = {
        "started_at": dt.datetime.now(dt.UTC).isoformat(),
        "mode": "reference_only" if args.reference_only else "llm",
        "model": settings.model,
        "embedding_model": settings.embedding_model,
        "temperature": 0,
        "seed": 42,
        "num_ctx": 8192,
        "num_predict": 1024,
        "reasoning": False,
        "few_shot_k": settings.few_shot_k,
        "max_iterations": settings.max_iterations,
        "max_tool_calls": settings.max_tool_calls,
        "top_k": settings.max_rows,
        "statement_timeout_ms": settings.statement_timeout_ms,
        "python": platform.python_version(),
        "platform": platform.platform(),
        "packages": {
            name: version(name) for name in ["text2sql", "langchain-core", "langchain-ollama"]
        },
    }
    if agent:
        try:
            with urlopen(settings.ollama_url + "/api/tags", timeout=5) as response:
                tags = json.load(response)["models"]
            metadata["model_digests"] = {
                item["name"]: item["digest"]
                for item in tags
                if item["name"]
                in {settings.model, settings.embedding_model, settings.embedding_model + ":latest"}
            }
        except (OSError, ValueError, KeyError):
            metadata["model_digests"] = {}
    records = []
    for case in cases:
        start = perf_counter()
        record = dict(case)
        expected = db.execute(case["reference_sql"], top_k=settings.max_rows)
        if expected.truncated:
            raise ValueError("Reference result was truncated; increase max_rows.")
        record["expected_rows"] = expected.rows
        if agent:
            try:
                result = agent.invoke(case["question"], top_k=settings.max_rows)
                record["actual"] = result.model_dump()
                record["correct"] = not result.result.truncated and same_rows(
                    expected.rows, result.result.rows, ordered=case["ordered"]
                )
            except AgentError as exc:
                record["correct"] = False
                record["error"] = {"code": exc.code, "message": exc.message}
                if exc.execution:
                    record["execution"] = exc.execution.model_dump()
        else:
            record["reference_valid"] = True
        record["elapsed_seconds"] = round(perf_counter() - start, 3)
        records.append(record)
        print(
            f"{case['id']}: {record.get('correct', 'reference ok')} ({record['elapsed_seconds']}s)",
            flush=True,
        )
        # Preserve real progress if a manual run is interrupted.
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps({"metadata": metadata, "cases": records}, indent=2) + "\n"
        )
    summary = {"cases": len(records)}
    if agent:
        summary.update(
            {
                "correct": sum(r["correct"] for r in records),
                "median_seconds": round(
                    statistics.median(r["elapsed_seconds"] for r in records), 3
                ),
                "corrections": sum(
                    r.get("actual", {})
                    .get("execution", r.get("execution", {}))
                    .get("corrections", 0)
                    for r in records
                ),
            }
        )
    args.output.write_text(
        json.dumps({"metadata": metadata, "summary": summary, "cases": records}, indent=2) + "\n"
    )
    print(json.dumps(summary))


if __name__ == "__main__":
    main()
