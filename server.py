from fastapi import FastAPI
from src.core.pipeline import RAGPipeline
from src.ocr.kvp_extract import OCRKVPExtractor
from src.models.base import QueryRequest, QueryResponse, DocumentAddRequest, DocumentAddResponse, OCRKVPResponse, OCRKVPRequest
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

app = FastAPI(title="RAG API with Classes & Pydantic")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pipeline = RAGPipeline()
ocr_kvp=OCRKVPExtractor()

@app.post("/query", response_model=QueryResponse)
async def query_rag(req: QueryRequest):
    context, answer = pipeline.run(req.prompt)
    return QueryResponse(source_documents=context, response=answer)

@app.post("/add_docs", response_model=DocumentAddResponse)
async def add_docs(req: DocumentAddRequest):
    count = pipeline.db_client.add_documents(req.documents)
    return DocumentAddResponse(status="success", count=count)

@app.post("/ocr_kvp",response_model=OCRKVPResponse)
async def ocr_kvp_extraction(req: OCRKVPRequest):
    kvp_extract = ocr_kvp.ocr_kvp_extraction_with_layout(image_path=req.image_path)
    return {"kvp_extraction": kvp_extract}

@app.post("/ocr_kvp_add_docs",response_model=OCRKVPResponse)
async def ocr_kvp_extraction_add_docs(req: OCRKVPRequest):
    upload_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    kvp_extract = ocr_kvp.ocr_kvp_extraction_with_layout(image_path=req.image_path)
    kvp_input=str(kvp_extract)
    document = [{"id": "kvp_" + upload_time, "content": kvp_input}]
    if kvp_extract:
        add_docs_response = await add_docs(DocumentAddRequest(documents=document))
        return {"kvp_extraction": kvp_extract, "add_docs": add_docs_response}
    return {"kvp_extraction": kvp_extract}