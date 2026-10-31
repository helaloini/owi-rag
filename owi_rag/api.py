import os
from functools import cache

from fastapi import FastAPI
from pydantic import BaseModel

from .agent import ask
from .llm import chat

app = FastAPI(title="owi-rag")


@cache
def retriever():
    from .retrieve import Retriever

    return Retriever(os.getenv("OWI_DATA", "data"))


class Ask(BaseModel):
    question: str


@app.get("/search")
def search(q: str, mode: str = "hybrid", k: int = 10):
    return retriever().search(mode, q, k)


@app.post("/ask")
def ask_endpoint(body: Ask):
    r = ask(body.question, retriever(), chat)
    r.pop("evidence")
    return r
