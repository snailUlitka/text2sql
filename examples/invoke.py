"""Run from the repository root: uv run python examples/invoke.py."""

import json

from text2sql import Settings
from text2sql.runtime import build_agent


def main():
    agent = build_agent(Settings())
    result = agent.invoke("Print the first 5 names of the passengers, sorted by name", top_k=5)
    print(json.dumps(result.model_dump(), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
