from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Finance Tracking App"
    collection_name: str = "financialRAG_records"
    database_name: str = "finance_db"
    chroma_port: int=8003
    chroma_host:str = "localhost"
    ollama_model_name:str ="deepseek-r1:8b"
    embed_model_name:str ="mxbai-embed-large"
    
    ocr_model_path: str = "/home/sinju/Documents/Fuse_locked/Ocr/fine"
    
    
    
    
    
settings = Settings()