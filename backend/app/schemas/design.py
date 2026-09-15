from pydantic import BaseModel,Field
from datetime import datetime

class DesignInsightOut(BaseModel):
    id:int
    asset_id:int
    page:str=""
    module:str=""
    feature:str
    description:str=""
    acceptance_criteria:str =""
    constraints:str=""
    priority:str="P1"
    sort_order:int=0
    selected:bool=True
    merged:bool=False

    model_config={"from_attributes":True}

class DesignInsightUpdate(BaseModel):
    page:str | None = None
    module:str | None = None
    feature:str | None = Field(default=None,min_length=1,max_length=200)
    description:str | None = None
    acceptance_criteria:str| None = None
    constraints:str | None = None
    priority:str | None = None
    selected:bool | None = None

class DesignMergeRequest(BaseModel):
    insight_ids: list[int] =[]

class DesignAssetOut(BaseModel):
    id:int
    project_id:int
    document_id:int
    asset_type:str
    title:str=""
    filename:str=""
    content_type:str=""
    figma_url:str=""
    status:str
    error_message:str =""
    parse_source:str=""
    image_summary:str=""
    created_at:datetime
    insights:list[DesignInsightOut]=[]

    model_config = {"from_attributes":True}

class FigmaLinkCreate(BaseModel):
    document_id:int
    url:str=Field(...,min_length=1,max_length=1000)
    title:str=Field(default="",max_length=200)