"""PostgreSQL access under a separate read-only login and bounded transactions."""

import datetime as dt
import json
from decimal import Decimal
from typing import Any

import psycopg
import sqlglot
from sqlglot import exp

from text2sql.schemas import AgentError, QueryResult


def json_value(value: Any) -> Any:
    if isinstance(value, (dt.datetime, dt.date, dt.time)):
        return value.isoformat()
    if isinstance(value, dt.timedelta):
        return value.total_seconds()
    if isinstance(value, Decimal):
        return str(value)
    if isinstance(value, bytes):
        return value.hex()
    return value


def read_query(sql: str) -> str:
    try:
        statements = sqlglot.parse(sql, read="postgres")
    except sqlglot.errors.ParseError:
        raise AgentError("invalid_sql", "SQL could not be parsed as PostgreSQL.") from None
    if len(statements) != 1 or not isinstance(statements[0], (exp.Select, exp.SetOperation)):
        raise AgentError("read_only", "Only one SELECT query is allowed.")
    tree = statements[0]
    if any(
        isinstance(node, (exp.DML, exp.DDL, exp.Into, exp.Lock, exp.Command))
        for node in tree.walk()
    ):
        raise AgentError("read_only", "Modifying SQL and locking clauses are not allowed.")
    return tree.sql(dialect="postgres")


class Database:
    def __init__(self, url: str, *, max_rows: int = 100, statement_timeout_ms: int = 3000):
        if not 1 <= max_rows <= 1000 or not 1 <= statement_timeout_ms <= 30000:
            raise ValueError("Invalid database limits.")
        self._url = url
        self.max_rows = max_rows
        self.statement_timeout_ms = statement_timeout_ms
        self.schema = ""

    def _connect(self):
        # These settings apply to each connection; there is no pooled SET ROLE assumption.
        try:
            return psycopg.connect(
                self._url,
                connect_timeout=5,
                options=(
                    f"-c statement_timeout={self.statement_timeout_ms} "
                    "-c default_transaction_read_only=on -c search_path=public,pg_catalog"
                ),
            )
        except psycopg.Error:
            raise AgentError("database_unavailable", "PostgreSQL connection failed.") from None

    def initialize(self) -> None:
        """Inspect the explicitly supplied DB; reject privileged or table-owning logins."""
        with self._connect() as conn:
            role = conn.execute(
                "SELECT rolsuper, rolcreatedb, rolcreaterole, rolreplication, rolbypassrls "
                "FROM pg_roles WHERE rolname = current_user"
            ).fetchone()
            unsafe = conn.execute(
                "SELECT EXISTS (SELECT 1 FROM pg_tables WHERE schemaname = 'public' AND "
                "(tableowner = current_user OR has_table_privilege("
                "current_user, quote_ident(schemaname)||'.'||quote_ident(tablename), "
                "'INSERT,UPDATE,DELETE,TRUNCATE,TRIGGER')))"
            ).fetchone()[0]
            memberships = conn.execute(
                "SELECT EXISTS (SELECT 1 FROM pg_auth_members m JOIN pg_roles r ON r.oid=m.roleid "
                "WHERE m.member=(SELECT oid FROM pg_roles WHERE rolname=current_user) "
                "AND (r.rolsuper OR r.rolcreatedb OR r.rolcreaterole OR r.rolbypassrls))"
            ).fetchone()[0]
            if any(role) or unsafe or memberships:
                raise AgentError(
                    "unsafe_database_role", "Use a separate SELECT-only database login."
                )
            rows = conn.execute(
                "SELECT table_name, column_name, data_type FROM information_schema.columns "
                "WHERE table_schema = 'public' ORDER BY table_name, ordinal_position"
            ).fetchall()
            if not rows:
                raise AgentError("empty_schema", "No readable tables found in the public schema.")
            tables: dict[str, list[str]] = {}
            for table, column, dtype in rows:
                tables.setdefault(table, []).append(f"{column} {dtype}")
            self.schema = "\n".join(f"{table}({', '.join(cols)})" for table, cols in tables.items())

    def execute(self, sql: str, *, top_k: int) -> QueryResult:
        if not 1 <= top_k <= self.max_rows:
            raise AgentError("row_limit", f"top_k must be between 1 and {self.max_rows}.")
        query = read_query(sql)
        # SQL LIMIT bounds work returned by the server, fetchmany bounds client materialization.
        effective = f"SELECT * FROM ({query}) AS text2sql_result LIMIT {top_k + 1}"
        try:
            with self._connect() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(effective)
                    columns = [col.name for col in cursor.description]
                    rows = [[json_value(v) for v in row] for row in cursor.fetchmany(top_k + 1)]
        except psycopg.errors.QueryCanceled:
            raise AgentError("statement_timeout", "SQL exceeded the statement timeout.") from None
        except psycopg.Error as exc:
            # Do not expose the connection string, full exception, context or server logs.
            detail = exc.diag.message_primary or "SQL execution failed."
            raise AgentError("sql_error", detail[:350]) from None
        result = QueryResult(
            sql=query, columns=columns, rows=rows[:top_k], truncated=len(rows) > top_k
        )
        if len(json.dumps(result.model_dump(), default=str)) > 20000:
            raise AgentError(
                "result_size", "Result exceeds 20,000 characters; select fewer columns."
            )
        return result
