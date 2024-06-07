"""Server for text2sql app based on LangServe"""
import os
from typing import (
    Any
)

from llm_app import get_ollamafunctions_agent

from pydantic import (
    BaseModel,
    Field
)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from langsmith import Client


from fastapi import FastAPI


os.environ["LANGCHAIN_PROJECT"] = "text2sql"
client = Client()


class InvokeInput(BaseModel):
    input: str
    top_k: int = Field(default=20)


class Output(BaseModel):
    output: Any


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

agent = get_ollamafunctions_agent().get_runnable()


@app.post("/text2sql/v1/invoke")
def agent_invoke(request: InvokeInput):
    return {"output": agent.invoke({
        "input": request.input,
        "top_k": 20  # request.top_k
    })}


def get_fastapi_app():
    return app
