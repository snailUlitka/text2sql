import json

import pytest
from langchain_core.messages import AIMessage, ToolMessage
from langchain_core.tools import tool

from text2sql import AgentError, SQLAgent
from text2sql.schemas import QueryResult


class ScriptedModel:
    def __init__(self, responses):
        self.responses = iter(responses)
        self.messages = []
        self.tools = []

    def bind_tools(self, tools):
        self.tools = tools
        return self

    def invoke(self, messages):
        self.messages = list(messages)
        return next(self.responses)


class FakeDatabase:
    schema = "passenger(passenger_name text)"
    max_rows = 100

    def __init__(self):
        self.calls = []

    def execute(self, sql, *, top_k):
        self.calls.append((sql, top_k))
        if sql == "SELECT name FROM passenger":
            raise AgentError("sql_error", "column name does not exist")
        return QueryResult(sql=sql, columns=["passenger_name"], rows=[["Alice"]])


def calls(*items):
    return AIMessage(
        content="",
        tool_calls=[
            {"name": name, "args": args, "id": f"call{i}", "type": "tool_call"}
            for i, (name, args) in enumerate(items)
        ],
    )


def test_dispatch_repairs_sql_and_passes_top_k():
    db = FakeDatabase()
    model = ScriptedModel(
        [
            calls(("query_sql", {"sql": "SELECT name FROM passenger"})),
            calls(("query_sql", {"sql": "SELECT passenger_name FROM passenger"})),
            AIMessage(content="<think>private</think>Alice"),
        ]
    )
    result = SQLAgent(model=model, database=db).invoke("Show a passenger", top_k=1)
    assert [limit for _, limit in db.calls] == [1, 1]
    assert result.answer == "Alice"
    assert result.execution.corrections == result.execution.sql_errors == 1
    assert result.execution.iterations == 3
    observations = [json.loads(m.content) for m in model.messages if isinstance(m, ToolMessage)]
    assert observations[0]["code"] == "sql_error"
    assert observations[1]["rows"] == [["Alice"]]


def test_extra_tool_dispatch_and_argument_validation():
    invoked = []

    @tool
    def note(value: str) -> str:
        """Record a test note."""
        invoked.append(value)
        return value

    model = ScriptedModel(
        [
            calls(
                ("missing", {}),
                ("query_sql", {"sql": 17}),
                ("query_sql", {"sql": "SELECT 1", "unexpected": True}),
                ("note", {"value": "ok"}),
                ("query_sql", {"sql": "SELECT 1"}),
            ),
            AIMessage(content="Alice"),
        ]
    )
    db = FakeDatabase()
    SQLAgent(model=model, database=db, extra_tools=[note]).invoke("Find data")
    assert invoked == ["ok"]
    assert db.calls == [("SELECT 1", 20)]
    observations = [json.loads(m.content) for m in model.messages if isinstance(m, ToolMessage)]
    assert [x["code"] for x in observations[:3]] == [
        "unknown_tool",
        "invalid_arguments",
        "invalid_arguments",
    ]


@pytest.mark.parametrize(
    "responses,limits,code",
    [
        ([calls(("database_schema", {}))], {"max_iterations": 1}, "iteration_limit"),
        (
            [calls(("database_schema", {}), ("database_schema", {}))],
            {"max_tool_calls": 1},
            "tool_limit",
        ),
        ([AIMessage(content="Invented answer")], {}, "no_sql_result"),
        (
            [AIMessage(content="partial", response_metadata={"done_reason": "length"})],
            {},
            "model_output_limit",
        ),
    ],
)
def test_budgets_and_missing_evidence(responses, limits, code):
    with pytest.raises(AgentError) as error:
        SQLAgent(model=ScriptedModel(responses), database=FakeDatabase(), **limits).invoke("test")
    assert error.value.code == code


def test_failed_latest_query_does_not_return_stale_evidence():
    model = ScriptedModel(
        [
            calls(("query_sql", {"sql": "SELECT 1"})),
            calls(("query_sql", {"sql": "SELECT name FROM passenger"})),
            AIMessage(content="Invented answer"),
        ]
    )
    with pytest.raises(AgentError, match="successful SQL"):
        SQLAgent(model=model, database=FakeDatabase()).invoke("test")
