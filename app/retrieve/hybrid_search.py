from app.retrieve.bm25_search import bm25_search
from app.retrieve.semantic_search import semantic_search


def reciprocal_rank_fusion(result_lists, rrf_k=60):
    scores = {}
    documents = {}

    for results in result_lists:
        # Get the hits from the search results
        hits = results["hits"]["hits"]

        # Loop through the hits and calculate the RRF score for each document
        for rank, hit in enumerate(hits, start=1):
            doc_id = hit["_id"]

        # Calculate the RRF score for the document and update the scores dictionary
            scores[doc_id] = (
                scores.get(doc_id, 0)
                + 1 / (rrf_k + rank)
            )
        # Store the document in the documents dictionary for later retrieval
            documents[doc_id] = hit

    # sort the documents by their RRF scores in descending order and return the ranked list
    ranked_ids = sorted(
        scores,
        key=scores.get,
        reverse=True
    )

    # Unpack the ranked documents and their RRF scores into a list of dictionaries to return
    return [
        {
            **documents[doc_id],
            "rrf_score": scores[doc_id]
        }
        for doc_id in ranked_ids
    ]


def hybrid_search(query: str, k: int = 5):
    # Perform BM25 search
    bm25_results = bm25_search(query, k)

    # Perform semantic search
    semantic_results = semantic_search(query, k)

    reciprocal_ranked_results = reciprocal_rank_fusion(
        [bm25_results, semantic_results],
        rrf_k=60
    )

    # Hybrid can return more than 5 results, so we slice to return only the top k results
    return reciprocal_ranked_results[:k]