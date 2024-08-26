from fastapi import FastAPI
from app.llama_index import query_llm
from pydantic import BaseModel

app = FastAPI()


class Query(BaseModel):
    question: str


@app.post("/query/")
async def query_endpoint(query: Query):
    answer = query_llm(query.question)
    return {"answer": answer}
