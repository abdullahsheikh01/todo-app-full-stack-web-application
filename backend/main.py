from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from db import check_database_connection

app = FastAPI(
    title="Todo App API",
    description="FastAPI backend for Todo App - Phase II",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check() -> dict:
    """Health check endpoint returning server and database status."""
    is_connected, message = check_database_connection()
    return {
        "status": "ok",
        "database": message,
    }
