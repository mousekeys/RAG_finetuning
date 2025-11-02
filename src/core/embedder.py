from ..config import settings
import ollama

class Embedder:
    def __init__(self, model_name: str = settings.embed_model_name):
        self.model_name = model_name
        
        
    def get_embedding(self, query:str):
        response= ollama.embed(model=self.model_name, input=query)
        if response['embeddings'] is None:
            raise ValueError("Embedding generation failed.")
        return response['embeddings']
