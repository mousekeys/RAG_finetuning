from .embedder import Embedder
from .db_client import ChromaClient
from ..config import settings
from .generator import Generator
from .retriever import Retriever

class RAGPipeline:
    def __init__(self):
        self.retriever = Retriever()
        self.generator = Generator()
        self.embedder = Embedder()
        self.db_client = ChromaClient()

    def run(self, query: str, top_k: int = 5):
        context = self.retriever.retrieve(query=query, top_k=top_k)
        if not context:
            raise ValueError("No context retrieved for the given query.")
        response = self.generator.generate_respose(context=context, prompt=query)
        return context[0],response
    
    