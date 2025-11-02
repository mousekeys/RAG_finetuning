from ..config import settings
from .embedder import Embedder
import chromadb
import ollama
from typing import List, Optional
from ..models.base import Document

class ChromaClient:
    def __init__(self):
        self.client = chromadb.HttpClient(host=settings.chroma_host, port=settings.chroma_port)
        self.collection = self.client.get_or_create_collection(name=settings.collection_name)
        self.embedder = Embedder(model_name=settings.embed_model_name)
        
    def add_documents(self, documents:List[Document])->str:
        ids = [d.id for d in documents]
        docs = [d.content for d in documents]
        metas = [d.metadata for d in documents]
        embedding= self.embedder.get_embedding(docs)
        self.collection.add(
            ids=ids,
            embeddings=embedding,
            documents=docs,
            metadatas=metas if metas else None
        )
        return len(docs)
        
    def query_records(self, embeddings: list, top_k: int):
        return self.collection.query(
            query_embeddings=embeddings,
            n_results=top_k
        )