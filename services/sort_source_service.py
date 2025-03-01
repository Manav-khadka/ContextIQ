from typing import List
from sentence_transformers import SentenceTransformer
import numpy as np

class SortSourceService:
    def __init__(self):
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
    def sort_sources(self, query : str, search_results : List[dict]):
        relevent_docs = []
        query_embedding = self.embedding_model.encode(query)  # similarity cos 0 = a.b / |a|*|b|
        for result in search_results:
            content_embedding = self.embedding_model.encode(result["content"])
            similarity = np.dot(query_embedding, content_embedding)/(np.linalg.norm(query_embedding)*np.linalg.norm(content_embedding))
            result["relevence_score"] = similarity
            if similarity > 0.4:
                relevent_docs.append(result)
        relevent_docs = sorted(relevent_docs, key=lambda x: x["relevence_score"], reverse=True)
        print(relevent_docs)
        return relevent_docs