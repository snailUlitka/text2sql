"""
Provides access to the database according to the specified parameters 
`local_data.py` data for connection.
Data in `local_data.py` you can create using `local_data_template.py`
"""
from app.databases.local_data import (
    PASSWORD_FOR_LLM,
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USER
)

from langchain_community.utilities.sql_database import SQLDatabase


def get_db() -> SQLDatabase:
    CONNECTION_STRING = \
        "postgresql+psycopg://" +\
        f"{DB_USER}:{PASSWORD_FOR_LLM}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    db = SQLDatabase.from_uri(CONNECTION_STRING)
    db.run("SET ROLE pg_read_all_data")

    return db
