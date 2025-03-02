from typing import List
from sentence_transformers import SentenceTransformer
import numpy as np

class SortSourceService:
    def __init__(self):
        try:
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        except Exception as e:
            print(f"Error initializing SentenceTransformer: {e}")
        
    def sort_sources(self, query: str, search_results: List[dict]):
        try:
            relevent_docs = []
            query_embedding = self.embedding_model.encode(query)  # similarity cos 0 = a.b / |a|*|b|
            for result in search_results:
                try:
                    content_embedding = self.embedding_model.encode(result["content"])
                    similarity = float(np.dot(query_embedding, content_embedding) / (np.linalg.norm(query_embedding) * np.linalg.norm(content_embedding)))
                    result["relevence_score"] = similarity
                    if similarity > 0.4:
                        relevent_docs.append(result)
                except Exception as e:
                    print(f"Error processing result {result}: {e}")
            relevent_docs = sorted(relevent_docs, key=lambda x: x["relevence_score"], reverse=True)
            print(relevent_docs)
            return relevent_docs
        except Exception as e:
            print(f"Error in sort_sources: {e}")
            return []