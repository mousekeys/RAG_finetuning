from fastapi import FastAPI
from src.core.pipeline import RAGPipeline
from src.models.base import QueryRequest, QueryResponse, DocumentAddRequest, DocumentAddResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="RAG API with Classes & Pydantic")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pipeline = RAGPipeline()

@app.post("/query", response_model=QueryResponse)
async def query_rag(req: QueryRequest):
    context, answer = pipeline.run(req.prompt)
    return QueryResponse(source_documents=context, response=answer)

@app.post("/add_docs", response_model=DocumentAddResponse)
async def add_docs(req: DocumentAddRequest):
    count = pipeline.db_client.add_documents(req.documents)
    return DocumentAddResponse(status="success", count=count)
