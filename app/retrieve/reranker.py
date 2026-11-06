from sentence_transformers import CrossEncoder

# Load the model once when the module is imported
reranker = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L6-v2"
)


def rerank_results(question: str, results: list, top_k: int = 5):

    if not results:
        return []

    # Pair the question with every candidate passage
    pairs = [
        (question, result["_source"]["text"])
        for result in results
    ]

    # Assign relevance scores
    scores = reranker.predict(pairs)

    scored_results = []

    # Attach the score to each original result
    for result, score in zip(results, scores):
        scored_results.append({
            **result,
            "rerank_score": float(score)
        })

    # Sort highest relevance first
    scored_results.sort(
        key=lambda result: result["rerank_score"],
        reverse=True
    )

    return scored_results[:top_k]