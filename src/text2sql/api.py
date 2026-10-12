"""Thin API v2. Resource initialization happens in the ASGI lifespan."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from text2sql.agent import SQLAgent
from text2sql.config import Settings
from text2sql.runtime import build_agent
from text2sql.schemas import AgentError, InvokeRequest, InvokeResult


def create_app(*, agent: SQLAgent | None = None, settings: Settings | None = None) -> FastAPI:
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        # Starlette runs synchronous endpoints in its thread pool.
        from starlette.concurrency import run_in_threadpool

        app.state.agent = agent or await run_in_threadpool(build_agent, settings or Settings())
        yield
        app.state.agent = None

    app = FastAPI(title="text2sql", version="2.0", lifespan=lifespan)

    @app.exception_handler(AgentError)
    async def agent_error_handler(request, exc: AgentError):
        status = (
            503
            if exc.code in {"model_unavailable", "database_unavailable", "retrieval_unavailable"}
            else 422
        )
        return JSONResponse(
            status_code=status, content={"error": {"code": exc.code, "message": exc.message}}
        )

    @app.get("/health")
    def health():
        return {"status": "ok", "api_version": 2}

    @app.post("/text2sql/v2/invoke", response_model=InvokeResult)
    def invoke(request: InvokeRequest):
        return app.state.agent.invoke(request.input, top_k=request.top_k)

    return app


app = create_app()
