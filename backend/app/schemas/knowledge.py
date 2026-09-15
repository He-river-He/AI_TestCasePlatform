from pydantic import BaseModel,Field,ConfigDict
from datetime import datetime

class KnowledgeChunkOut(BaseModel):
    id:int 
    content:str
    heading:str = ""

    model_config = ConfigDict(from_attributes=True)

class KnowledgeDocumentCreate(BaseModel):
    title:str
    content:str
    source_type:str = "doc" # doc | case | defect

class KnowledgeDocumentOut(BaseModel):
    id:int
    project_id:int
    title:str
    source_type:str
    status:str
    error_message:str =""
    chunk_count:int =0
    created_at:datetime

    model_config=ConfigDict(from_attributes=True)

class KnowledgeSearchRequest(BaseModel):
    query:str
    top_k:int = 5

class KnowledgeSearchHit(BaseModel):
    content:str
    title:str = ""
    heading:str =""
    source_type:str = "doc"
    score:float = 0.0
    match:str = "vector" # vector 语义 / keyword 关键词 / both 双路命中