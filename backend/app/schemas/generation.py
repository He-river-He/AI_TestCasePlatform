from pydantic import BaseModel,Field
from datetime import datetime
from typing import Literal

class GeneratedCaseDraftOut(BaseModel):
    id: int
    requirement_item_id: int | None
    title: str
    priority: str
    case_type: str
    is_smoke: bool = False
    precondition: str
    steps: str
    expected_result: str
    quality_status: str
    quality_issues: str
    review_status: str
    reject_reason: str = ""
    was_edited: bool = False
    skill_name: str
    judge_score: float | None = None
    judge_issues: str = ""
    module: str = ""
    feature: str = ""

    model_config = {"from_attributes":True}

class QualityReportOut(BaseModel):
    id: int
    total_cases: int
    pass_count: int
    warning_count: int
    fail_count: int
    coverage_rate: float
    uncovered_features: str
    suggestions: str
    avg_judge_score: float | None = None
    hallucination_count: int = 0
    duplicate_count: int = 0

    model_config = {"from_attributes":True}


# --------------------------------------------------------------------------------
class ReviewStatsOut(BaseModel):
    total:int=0
    adopted:int=0
    rejected:int=0
    edited_adopted:int=0
    pending:int=0
    reviewed:bool=False
    adoption_rate:float=0.0
    edit_rate:float=0.0
    rejection_rate:float=0.0

# -----------------------------------------------------------------------------------
class ReviewAction(BaseModel):
    draft_ids:list[int]
    action:Literal["adopt","reject","to_confirm"]
    reject_reason:str = "" #驳回原因(badcase归因用)


# -----------------------------------------------------------------------------------
class DraftEdit(BaseModel):
    title:str | None = None
    priority:str | None = None
    case_type:str | None = None
    precondition:str | None = None
    steps:str | None=None
    expected_result:str | None = None

# --------------------------------------------------------------------------------

class GenerationTaskCreate(BaseModel):
    document_id:int
    strategy:str="full" # full | quick
    specialist_skills:list[str]=Field(
        default_factory=list,
        description="可选专项Skill: security(安全/权限)、api_test(接口测试)"
    )
    use_knowledge:bool=False

class GenerationTaskOut(BaseModel):
    id:int
    project_id:int
    document_id:int
    strategy:str
    strategy_config:str
    status:str
    progress:int
    stage:str=""
    error_message:str
    tokens_used:int=0
    knowledge_refs: str ="" # JSON: {item_id: [{title, heading, score}]}，RAG 溯源
    pause_requested: bool = False
    created_at:datetime
    updated_at:datetime
    drafts:list[GeneratedCaseDraftOut] =[]
    quality_report:QualityReportOut | None=None
    review_stats:ReviewStatsOut | None =None

    model_config = {"from_attributes":True}

class GenerationTaskSummaryOut(BaseModel):
    """生成记录列表项:不含草稿明细的轻量视图"""

    id:int
    document_id:int
    document_title:str=""
    strategy:str
    specialist_skills:list[str]=[]
    status:str
    progress:int
    error_message:str = ""
    tokens_used:int=0
    created_at:datetime
    draft_count:int=0
    smoke_count:int=0
    coverage_rate:float | None=None
    review_stats:ReviewStatsOut | None = None

