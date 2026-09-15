from pydantic import BaseModel,Field,model_validator
from datetime import datetime
from typing import Literal

class ExecutionStats(BaseModel):
    total: int
    passed: int
    failed: int
    blocked: int
    pending: int
    executed: int
    pass_rate: float

# ------------------------------------------------------------------------------------

class TestBatchCreate(BaseModel):
    name:str = Field(...,min_length=1,max_length=100)
    case_ids:list[int] = []
    copy_from_batch_id: int | None = None # 复用某个已有批次的用例集(结果重置)

    @model_validator(mode="after")
    def validate_case_source(self):
        if not self.case_ids and self.copy_from_batch_id is None:
            raise ValueError("请选择用例或指定要复用的批次")
        return self
    
class TestBatchUpdate(BaseModel):
    name:str = Field(...,min_length=1,max_length=100)
    status:Literal["in_progress","completed"] | None = None
    
class TestBatchOut(BaseModel):
    id: int
    task_id: int
    name: str
    status: str
    created_at: datetime
    updated_at: datetime
    stats: ExecutionStats

    model_config = {"from_attributes": True}

# ------------------------------------------------------------------------------------

class TestTaskCreate(BaseModel):
    name:str = Field(...,min_length=1,max_length=200)
    description:str =""
    batch_name:str = Field("线下测试",min_length=1,max_length=100) #首个批次名称
    case_ids:list[int] = []
    source_task_id:int | None = None #传入生成任务ID时,自动导入该任务已采纳入库的用例

    @model_validator(mode="after")
    def validate_case_source(self):
        if not self.case_ids and self.source_task_id is None:
            raise ValueError("请选择用例或指定生成任务")
        return self
    
class TestTaskUpdate(BaseModel):
    name: str | None = Field(None,min_length=1,max_digits=200)
    description: str | None = None
    status:Literal["in_progress","completed"] | None = None

class TestTaskOut(BaseModel):
    id: int
    project_id: int
    name: str
    description: str
    status: str
    created_at: datetime
    updated_at: datetime
    stats: ExecutionStats
    batches: list[TestBatchOut] = []

    model_config = {"from_attributes": True}

# -----------------------------------------------------------------------------------
class BatchCaseOut(BaseModel):
    id: int  # 执行记录 ID
    case_id: int
    title: str = ""
    priority: str = ""
    case_type: str = ""
    is_smoke: bool = False
    precondition: str = ""
    steps: str = ""
    expected_result: str = ""
    module: str = ""
    feature: str = ""
    result: str
    note: str
    defect_ref: str
    executed_at: datetime | None = None

class TestBatchDetailOut(TestBatchOut):
    cases: list[BatchCaseOut] = []

class BatchCaseMark(BaseModel):
    result: Literal["pending","passed","failed","blocked"]
    note: str = ""
    defect_ref:str = ""

class BatchCaseBatchMark(BaseModel):
    batch_case_ids: list[int] = Field(...,min_length=1)
    result: Literal["pending","passed","failed","blocked"]

class BatchCasesAdd(BaseModel):
    case_ids: list[int] = Field(...,min_length=1)

class DefectItemOut(BaseModel):
    batch_case_id: int
    batch_id: int
    batch_name: str
    case_id: int
    title: str = ""
    priority: str = ""
    module: str = ""
    feature: str = ""
    result: str
    note: str
    defect_ref: str
    executed_at: datetime | None = None