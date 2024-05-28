"""
Provides access to the database according to the specified parameters `local_data.py` data for connection.
Data in `local_data.py` you can create using `local_data_template.py`
"""
from app.databases.local_data import (
    PASSWORD_FOR_LLM,
    DB_USER,
    DB_NAME,
    DB_PORT
)

from langchain_community.vectorstores.pgvector import PGVector
from langchain_community.utilities.sql_database import SQLDatabase


def get_db() -> SQLDatabase:
    CONNECTION_STRING = PGVector.connection_string_from_db_params(
        driver="psycopg2",
        host="localhost",
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=PASSWORD_FOR_LLM
    )
    db = SQLDatabase.from_uri(CONNECTION_STRING)
    db.run("SET ROLE pg_read_all_data")

    return db


if __name__ == "__main__":
    print(get_db().run("select * from passenger"))
