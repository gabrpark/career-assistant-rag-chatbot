from llama_index import GPTIndex
from app.database import get_post_by_id

# Example: Fetch and index data from MongoDB


def query_llm(query):
    # Retrieve the full post based on sentence match
    response = qdrant_client.search(
        collection_name="posts",
        query_vector=model.encode(query).tolist(),
        limit=1
    )
    post_id = response[0].payload['post_id']
    full_post = get_post_by_id(post_id)

    # Use LLM to generate a response based on the full post
    llm = GPTIndex.from_text(full_post['post_text'])
    answer = llm.query(query)
    return answer
