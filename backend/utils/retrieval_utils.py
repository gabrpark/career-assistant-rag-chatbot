import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def split_text_into_chunks(text, chunk_size=500):
    paragraphs = re.split(r'\n\n+', text)
    chunks = []
    for paragraph in paragraphs:
        if len(paragraph) > chunk_size:
            sub_chunks = [paragraph[i:i+chunk_size]
                          for i in range(0, len(paragraph), chunk_size)]
            chunks.extend(sub_chunks)
        else:
            chunks.append(paragraph)
    return chunks


def retrieve_relevant_chunks(query, chunks):
    vectorizer = TfidfVectorizer().fit_transform(chunks)
    vectors = vectorizer.toarray()
    query_vec = vectorizer.transform([query]).toarray()
    similarity = cosine_similarity(query_vec, vectors).flatten()
    most_similar_idx = similarity.argsort()[-5:][::-1]
    return [chunks[i] for i in most_similar_idx]
