from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
from uuid import uuid4

# Initialize models and clients
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
qdrant_client = QdrantClient(host=os.getenv(
    "QDRANT_HOST"), port=os.getenv("QDRANT_PORT"))


def embed_and_store_post(post_text, post_id):
    sentences = post_text.split('. ')
    embeddings = model.encode(sentences)

    points = [
        PointStruct(
            id=uuid4().hex,
            vector=embedding.tolist(),
            payload={"post_id": post_id, "sentence": sentence}
        )
        for embedding, sentence in zip(embeddings, sentences)
    ]

    qdrant_client.upsert(
        collection_name="posts",
        points=points
    )
