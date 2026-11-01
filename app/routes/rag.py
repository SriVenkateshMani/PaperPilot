from fastapi import APIRouter
from pydantic import BaseModel
import json
from app.generation.generator import answer_question
from fastapi.responses import StreamingResponse
from app.cache.redis_client import set_cache

router = APIRouter(
    prefix="/rag",
    tags=["rag"]
)

# Pydantic validation for the incoming question
class QuestionRequest(BaseModel):
    question: str

# Format the stream and results into a JSON response
def format_stream(stream, results):
    for chunk in stream:
        full_answer = chunk  # Store the full answer for caching later

        yield json.dumps({
            "type": "chunk",
            "data": chunk
        }) + "\n"

    # Cache the full answer and results in Redis for future requests
    set_cache(
        question,
        json.dumps({
            "answer": full_answer,
            "results": results
        }),
    )
    sources = []

    for result in results:
        source = result["_source"]

        sources.append({
            "title": source["title"],
            "paper_id": source["paper_id"],
            "chunk_id": source["chunk_id"]
        })

    yield json.dumps({
        "type": "sources",
        "data": sources
    }) + "\n"

# Expose the /ask endpoint to handle question requests
@router.post("/ask")
def ask_question(request: QuestionRequest):
    stream, results = answer_question(request.question)

    return StreamingResponse(
        format_stream(stream, results),
        media_type="application/x-ndjson" # Set the media type to NDJSON - Newline Delimited JSON
    )