from app.retrieve.hybrid_search import hybrid_search
from app.cache.redis_client import get_cache, set_cache
from app.logger import get_logger
import requests
import json

logger = get_logger(__name__)

# Build a list of context to pass to the LLM from retrieved context
def build_context(results):
    context_parts = []
    for result in results:
        source = result["_source"]
        context_parts.append(source["text"])

    return "\n\n".join(context_parts)

# Retrieve the top-k relevant chunks and combine them into one context string
def retrieve_context(question: str, k: int = 5):
    results = hybrid_search(question, k)
    return build_context(results)

# Build the prompt ready to go into Ollama
def build_prompt(question: str, context: str):
    return f"""

    You are a research assistant.

    Answer the question using only the provided context.
    Do not invent definitions, acronyms, facts, or terminology.
    If the context does not contain enough information, say that clearly.

    Question: {question}

    Context: {context}

    Answer: 
    """

# Give the prompt to the model
def generate_answer(prompt: str):
    response = requests.post(
        "http://ollama:11434/api/generate",
        json={
            "model": "llama3.2",
            "prompt": prompt,
            "stream": False
        }
    )

    response.raise_for_status()

    data = response.json()

    return data["response"]

# Spit out stream as it generates
def generate_answer_stream(prompt: str):
    response = requests.post(
        "http://ollama:11434/api/generate",
        json={
            "model": "llama3.2",
            "prompt": prompt,
            "stream": True
        },
        stream=True
    )

    response.raise_for_status()

    # Read one line at a time from the stream and decode it and yield it
    for line in response.iter_lines():
        if line:
            # Decode the line and parse the JSON
            data = json.loads(line.decode("utf-8"))
            yield data["response"]

# Generate the answer
def answer_question(question: str, k: int = 5):
    # Handling redis caching for the question
    cached = get_cache(question)

    if cached:
        data = json.loads(cached)

        def cached_stream():
            yield data["answer"]

        return cached_stream(), data["results"]

    results = hybrid_search(question, k)

    context = build_context(results)
    prompt = build_prompt(question, context)

    answer = generate_answer_stream(prompt)

    return answer, results

# Invoke the generate answer function
if __name__ == "__main__":
    stream, results = answer_question(
        "What is the purpose of retrieval augmented generation?"
    )

    # Consume the pieces as they arrive 
    for chunk in stream:
        print(chunk, end="", flush=True)