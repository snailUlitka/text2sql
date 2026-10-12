from fastapi.testclient import TestClient

from text2sql.api import create_app
from text2sql.schemas import AgentError, ExecutionInfo, InvokeResult, QueryResult


class Agent:
    def invoke(self, question, *, top_k):
        if question == "fail":
            raise AgentError("model_unavailable", "Ollama request failed or timed out.")
        return InvokeResult(
            answer="Alice",
            sql="SELECT passenger_name FROM passenger",
            result=QueryResult(
                sql="SELECT passenger_name FROM passenger",
                columns=["passenger_name"],
                rows=[["Alice"]],
            ),
            execution=ExecutionInfo(
                iterations=2,
                tool_calls=1,
                sql_attempts=1,
                sql_errors=0,
                corrections=0,
                elapsed_seconds=0.01,
                example_ids=[str(top_k)],
            ),
        )


def test_v2_contract_limits_and_errors():
    with TestClient(create_app(agent=Agent())) as client:
        assert client.get("/health").json() == {"status": "ok", "api_version": 2}
        result = client.post("/text2sql/v2/invoke", json={"input": "Show names", "top_k": 3})
        assert result.status_code == 200
        assert result.json()["execution"]["example_ids"] == ["3"]
        assert set(result.json()) == {"answer", "sql", "result", "execution"}
        for body in [
            {"input": ""},
            {"input": "test", "top_k": 0},
            {"input": "test", "top_k": "3"},
            {"input": "test", "extra": True},
        ]:
            assert client.post("/text2sql/v2/invoke", json=body).status_code == 422
        error = client.post("/text2sql/v2/invoke", json={"input": "fail"})
        assert error.status_code == 503
        assert error.json()["error"]["code"] == "model_unavailable"
        assert client.post("/text2sql/v1/invoke", json={"input": "test"}).status_code == 404
