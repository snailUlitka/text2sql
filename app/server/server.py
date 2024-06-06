"""Server for text2sql app based on LangServe"""
import sys
import os
from typing import (
    Dict,
    Any
)

project_root = os.path.abspath(os.path.join(os.getcwd(), ".\\app"))
if project_root not in sys.path:
    sys.path.append(project_root)

from llm_app import get_ollamafunctions_agent

from langchain_core.pydantic_v1 import BaseModel

from langserve import add_routes
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from langsmith import Client


from fastapi import Depends, FastAPI, Request, Response
from langchain_core.runnables import RunnableLambda
from sse_starlette import EventSourceResponse

from langserve import APIHandler


os.environ["LANGCHAIN_PROJECT"] = "text2sql"
client = Client()


class Input(BaseModel):
    input: Any#Dict[str]


class Output(BaseModel):
    output: Any




def start_server():
    app = FastAPI(
        title="text2sql app server",
        version="1.0",
        description="Simple server based on LangServe",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )

    # add_routes(
    #     app,
    #     get_ollamafunctions_agent().get_runnable(),#.with_types(
    #     #     input_type=Input,
    #     #     output_type=Output
    #     # ),
    #     path="/text2sql/v1",
    #     enabled_endpoints=["invoke"]
    # )
    
    api_handler = APIHandler(get_ollamafunctions_agent().get_runnable(), 
                             path="/text2sql/v1")
    
    @app.post("/text2sql/v1/invoke", include_in_schema=False)
    async def simple_invoke(request: Request) -> Response:
        """Handle a request."""
        # The API Handler validates the parts of the request
        # that are used by the runnnable (e.g., input, config fields)
        return await api_handler.invoke(request)
    
    
    return app

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(start_server(), host="localhost", port=8000)
    
    
