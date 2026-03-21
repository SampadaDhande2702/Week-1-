import numpy as np
from rank_bm25 import BM25Okapi
from sentence_transformers import CrossEncoder

#CrossEncoder is a type of AI model that reads two pieces of text together and outputs a single relevance score.
reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

def hybrid_search(query, collection, embedder, top_k=6):
    total = collection.count()
    if total == 0:
        return []


    # Vector search

    #1)It encodes our query
    query_embedding = embedder.encode(query).tolist()
    n = max(1, min(top_k, total))


    #This will actually search the query on chromadb and return the most relevant chunks based on cosine similarity of embeddings
    vector_results = collection.query(query_embeddings=[query_embedding], n_results=n)

    #MAtching text info
    vector_chunks = vector_results["documents"][0]
    #Their places
    vector_metas  = vector_results["metadatas"][0]



    # BM25 keyword search
    #Stores whole data from db
    all_data  = collection.get()

    #Stores documents / text chunks
    all_docs  = all_data["documents"]

    #Stores the place of chunk
    all_metas = all_data["metadatas"]

    tokenized = [d.lower().split() for d in all_docs if d.strip()]
    if not tokenized:
        return []


    bm25 = BM25Okapi(tokenized)#Figures out which words are rare and which words are common

    scores = bm25.get_scores(query.lower().split())#Takes our query and scores every single document according to it

    top_idx = np.argsort(scores)[-top_k:][::-1]

    combined_chunks = list(vector_chunks)
    combined_metas  = list(vector_metas)
    for idx in top_idx:
        if all_docs[idx] not in combined_chunks:
            combined_chunks.append(all_docs[idx])
            combined_metas.append(all_metas[idx])

    # Re-rank

    #The combination of documents and query
    pairs  = [(query, c) for c in combined_chunks]

    #It predicts scores according to all docs and query
    ranked_scores = reranker.predict(pairs)
    ranked = sorted(zip(ranked_scores, combined_chunks, combined_metas), key=lambda x: x[0], reverse=True)
    return ranked[:top_k]