import os

import psycopg
import pytest

from text2sql import AgentError, Database
from text2sql.database import read_query


@pytest.mark.parametrize(
    "sql",
    [
        "DELETE FROM passenger",
        "SELECT 1; SELECT 2",
        "SELECT * INTO copied FROM passenger",
        "WITH d AS (DELETE FROM passenger RETURNING *) SELECT * FROM d",
        "SELECT * FROM passenger FOR UPDATE",
        "COPY passenger TO STDOUT",
    ],
)
def test_rejects_modifying_and_multiple_statements(sql):
    with pytest.raises(AgentError):
        read_query(sql)


def test_read_query_allows_cte_and_union():
    assert "WITH" in read_query("WITH p AS (SELECT 1 AS n) SELECT n FROM p UNION SELECT 2")


@pytest.mark.db
def test_postgres_permissions_timeout_and_result_limits():
    url = os.getenv("TEXT2SQL_TEST_DATABASE_URL")
    if not url:
        pytest.skip("Set TEXT2SQL_TEST_DATABASE_URL to run the Compose DB smoke test.")
    db = Database(url, statement_timeout_ms=100, max_rows=5)
    db.initialize()
    result = db.execute("SELECT passenger_name FROM passenger ORDER BY passenger_name", top_k=2)
    assert result.rows == [["Alice"], ["Bob"]]
    assert result.truncated
    with pytest.raises(AgentError) as timeout:
        db.execute("SELECT pg_sleep(1)", top_k=1)
    assert timeout.value.code == "statement_timeout"
    with pytest.raises(AgentError) as limit:
        db.execute("SELECT 1", top_k=6)
    assert limit.value.code == "row_limit"
    # Check actual grants independently of the SQL parser and read-only transaction setting.
    with psycopg.connect(url, autocommit=True) as conn:
        conn.execute("SET default_transaction_read_only = off")
        with pytest.raises(psycopg.errors.InsufficientPrivilege):
            conn.execute("DELETE FROM passenger WHERE false")
        with pytest.raises(psycopg.errors.InsufficientPrivilege):
            conn.execute("CREATE TABLE public.denied (n int)")
