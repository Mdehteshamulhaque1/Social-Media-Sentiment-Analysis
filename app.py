"""Convenience launcher for the FastAPI service."""

from backend.fastapi_service.app.main import app


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("backend.fastapi_service.app.main:app", host="0.0.0.0", port=8000, reload=True)