from .embedder import Embedder
from .db_client import ChromaClient
from ..config import settings


class Retriever:
    def __init__(self, embed_model_name:str = settings.embed_model_name):
        self.embed_model_name = embed_model_name
        self.db_client = ChromaClient()
        
    def get_embedding(self, query:str):
        embedder=Embedder(model_name=self.embed_model_name)
        return embedder.get_embedding(query=query)
    
    def retrieve(self, query:str, top_k:int=5):
        embedding = self.get_embedding(query=query)
        results = self.db_client.query_records(embeddings=embedding, top_k=top_k)
        if results['documents'] is None:
            raise ValueError("No results retrieved from database.") 
        return results["documents"]
        