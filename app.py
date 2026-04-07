from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from pydantic import BaseModel, Field

from src.generation import build_support_answer


BASE_DIR = Path(__file__).resolve().parent
app = FastAPI(title="Student Support Copilot", version="0.1.0")


class SupportRequest(BaseModel):
    question: str = Field(..., min_length=8)
    top_k: int = Field(default=3, ge=1, le=5)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/support")
def support(request: SupportRequest) -> dict:
    return build_support_answer(BASE_DIR, question=request.question, top_k=request.top_k)
