from pydantic import BaseModel,Field
from datetime import datetime

class EvalCheckpoint(BaseModel):
    text: str
    keywords: list[str] =[]

class EvalSampleCreate(BaseModel):
    title:str
    content:str
    checkpoints:list[EvalCheckpoint] = []

class EvalSampleUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    checkpoints:list[EvalCheckpoint] | None = None

class EvalSampleOut(BaseModel):
    id:int 
    project_id:int
    title:str
    content:str
    checkpoints: list[EvalCheckpoint] = []
    created_at:datetime

class EvalRunCreate(BaseModel):
    label: str
    sample_ids: list[int]
    strategy: str ="full"

class EvalResultOut(BaseModel):
    id:int
    sample_id:int
    sample_title:str=""
    task_id:int | None=None
    status: str
    metrics:dict ={}

class EvalRunOut(BaseModel):
    id:int
    project_id:int
    label:str
    config:dict ={}
    status:str
    progress:int
    stage:str=""
    error_message:str=""
    metrics:dict={}
    created_at:datetime
    results:list[EvalResultOut] =[]