from pydantic import BaseModel,Field
from datetime import datetime
from typing import Literal

class ProjectCreate(BaseModel):
    name:str=Field(...,min_length=1,max_length=200)
    description:str=""

class ProjectUpdate(BaseModel):
    name:str | None=None
    description:str | None=None

class ProjectOut(BaseModel):
    id:int
    user_id:int
    name:str
    description:str
    created_at:datetime
    updated_at:datetime

    # 这个响应模型可以直接把 SQLAlchemy 的 Project 对象转换成 Pydantic 的 ProjectResponse
    model_config = {"from_attributes":True}

# ------------------项目统计/阶段响应-----------------------------
class ProjectStatsOut(BaseModel):
    id: int
    name: str
    description: str
    created_at: datetime
    updated_at: datetime
    testcase_count: int = 0
    generation_count: int = 0
    last_generation_at: datetime | None = None
    last_generation_status: str | None = None

class ProjectStageOut(BaseModel):
    """项目当前所处的真实工作阶段，用于工作台与「继续工作」入口。

    stage: import（导入需求）→ confirm（确认功能点）→ generate（AI 生成）
           → review（人工评审）→ done（用例入库）
    """

    stage: Literal["import", "confirm", "generate", "review", "done"]
    document_id: int | None = None
    document_title: str = ""
    task_id: int | None = None
    generating: bool = False
    failed: bool = False
    paused: bool = False
    pending_drafts: int = 0
    item_count: int = 0
    testcase_count: int = 0

class HomeOverviewOut(BaseModel):
    total_projects: int
    total_testcases: int
    total_generations: int
    projects: list[ProjectStatsOut]
    latest_active_project_id: int | None = None
    latest_active_stage: ProjectStageOut | None = None