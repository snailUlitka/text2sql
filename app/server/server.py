"""Server for text2sql app based on LangServe"""
from langserve import add_routes
from fastapi import FastAPI
from llm_app import get_ollamafunctions_agent
import sys
import os


project_root = os.path.abspath(os.path.join(os.getcwd(), ".\\app"))
if project_root not in sys.path:
    sys.path.append(project_root)


app = FastAPI(
    title="text2sql app server",
    version="1.0",
    description="Simple server based on LangServe",
)

add_routes(
    app,
    get_ollamafunctions_agent().get_runnable(),
    path="/text2sql/v1"
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
