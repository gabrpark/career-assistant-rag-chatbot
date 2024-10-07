# Function to perform similarity search based on cosine similarity
def find_most_similar_chunks(query_embedding, chunk_embeddings, chunks, top_n=3):
    similarities = []
    for i, embedding in enumerate(chunk_embeddings):
        similarity = cosine_similarity(query_embedding, embedding)
        similarities.append((similarity, chunks[i]))
    similarities.sort(reverse=True, key=lambda x: x[0])
    return [chunk for _, chunk in similarities[:top_n]]