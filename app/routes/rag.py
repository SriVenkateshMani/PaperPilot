from fastapi import APIRouter
from pydantic import BaseModel

from app.generation.generator import answer_question
from fastapi.responses import StreamingResponse

router = APIRouter(
    prefix="/rag",
    tags=["rag"]
)

# Pydantic validation for the incoming question
class QuestionRequest(BaseModel):
    question: str

# Endpoint to ask a question and get an answer
@router.post("/ask")
def ask_question(request: QuestionRequest):
    stream, results = answer_question(request.question)

    sources = []

    for result in results:
        source = result["_source"]
        sources.append({
            "title": source["title"],
            "paper_id": source["paper_id"],
            "chunk_id": source["chunk_id"]
        })

    return {
        "question": request.question,
        "answer": answer,
        "sources": sources
    }