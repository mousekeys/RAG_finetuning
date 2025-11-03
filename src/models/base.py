from pydantic import BaseModel, Field
from typing import List, Optional

class QueryRequest(BaseModel):
    prompt:str = Field(..., description="The prompt to query financial records.")
    top_k: int = Field(5, description="Number of top records to retrieve.")
    
class QueryResponse(BaseModel):
    source_documents: Optional[List[str]] = Field(..., description="Optional source documents related to the query.")
    response:str = Field(..., description="The response generated based on the query and retrieved records.")

class Document(BaseModel):
    id: str = Field(..., description="Unique identifier for the document.")
    content: str = Field(..., description="The content of the document to be added.")
    metadata: Optional[dict] = Field(None, description="Optional metadata for the document.")

class DocumentAddRequest(BaseModel):
    documents: List[Document] 
    
class DocumentAddResponse(BaseModel):
    status: str = Field(..., description="Status of the add record operation.")
    count: int = Field(..., description="Number of records added successfully.")
    
class OCRKVPResponse(BaseModel):
    kvp_extraction: dict = Field(..., description="Key-Value pairs extracted from the OCR process.")
    
class OCRKVPRequest(BaseModel):
    image_path: str = Field(..., description="Path to the image for OCR KVP extraction.")