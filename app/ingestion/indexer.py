from opensearchpy import OpenSearch
from app.logger import get_logger

logger = get_logger(__name__)

# Create a client 
client = OpenSearch(
    hosts = [
        {
            "host": "opensearch",
            "port": 9200
        }
    ],
    use_ssl = False
)


INDEX_NAME = "paper_chunks"

# Create the mappping
def create_index():
    mapping = {
        "settings":{
            "index":{
                "knn": True
            }
        },

        "mappings":{
            "properties":{
                "paper_id":{
                    "type": "keyword"
                },
                "title":{
                    "type": "text"
                },
                "chunk_id":{
                    "type": "integer"
                },
                "text":{
                    "type": "text"
                },
                "embedding":{
                    "type": "knn_vector",
                    "dimension": 384
                }
            }
        }
    }

    if client.indices.exists(index = INDEX_NAME):
        logger.info(f"Index {INDEX_NAME} already exists")
        return

    client.indices.create(
        index = INDEX_NAME,
        body = mapping
    )

    logger.info(f"Created index: {INDEX_NAME}")


# Populate the index
def index_chunks(paper, embeddings, chunks):
    for chunk_id, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        document = {
            "paper_id": paper.entry_id,
            "title": paper.title,
            "chunk_id": chunk_id,
            "text": chunk,
            "embedding": embedding.tolist()
        }

        client.index(
            index = INDEX_NAME,
            body = document
        )

    logger.info(f"Indexed {len(chunks)} chunks into {INDEX_NAME}")