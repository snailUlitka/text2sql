from server import get_fastapi_app


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(get_fastapi_app(), host="localhost", port=8000)
    