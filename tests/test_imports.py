import subprocess
import sys


def test_imports_do_not_construct_external_resources():
    code = """
import ollama
import psycopg
def forbidden(*args, **kwargs):
    raise AssertionError("External resource constructed during import")
psycopg.connect = forbidden
ollama.Client.__init__ = forbidden
ollama.AsyncClient.__init__ = forbidden
import text2sql
import text2sql.api
import text2sql.runtime
import text2sql.evaluation
"""
    subprocess.run([sys.executable, "-c", code], check=True, capture_output=True)
