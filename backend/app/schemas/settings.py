from pydantic import BaseModel
from typing import Literal

class SystemSettingsOut(BaseModel):
    llm_api_key_set:bool
    llm_api_key_masked:str =""
    llm_base_url:str =""
    llm_model:str =""
    llm_mock_mode:bool 
    vision_api_key_set:bool =False
    vision_api_key_masked:str =""
    vision_base_url:str =""
    vision_model:str =""
    embedding_api_key_set:bool=False
    embedding_api_key_masked:str =""
    embedding_base_url:str =""
    embedding_model:str =""
    rerank_api_key_set:bool=False
    rerank_api_key_masked:str =""
    rerank_base_url:str =""
    rerank_model:str =""
    eval_llm_api_key_set:bool = False
    eval_llm_api_key_masked:str = ""
    eval_llm_base_url:str = ""
    eval_llm_model:str = ""

class SystemSettingsUpdate(BaseModel):
    llm_api_key:str | None = None
    llm_base_url:str | None = None
    llm_model:str | None = None
    llm_mock_mode:bool | None = None
    vision_api_key:str | None = None
    vision_base_url:str | None = None
    vision_model:str | None = None
    embedding_api_key: str | None = None
    embedding_base_url: str | None = None
    embedding_model: str | None = None
    rerank_api_key: str | None = None
    rerank_base_url: str | None = None
    rerank_model: str | None = None
    eval_llm_api_key: str | None = None
    eval_llm_base_url: str | None = None
    eval_llm_model: str | None = None



class SettingsTestRequest(BaseModel):
    target: Literal["generation","vision","eval","embedding","rerank"] ="generation"

class SettingsTestOut(BaseModel):
    ok:bool
    message:str =""
    model:str =""
    base_url:str =""