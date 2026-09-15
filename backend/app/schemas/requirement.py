from pydantic import BaseModel,Field
from datetime import datetime

class RequirementItemCreate(BaseModel):
    module:str = ""
    feature:str = Field(...,min_length=1,max_length=200)
    description:str = ""
    acceptance_criteria:str = ""
    constraints:str = ""
    priority:str = "P1"

class RequirementItemUpdate(BaseModel):
    module:str | None = None
    feature:str | None = None
    description:str | None = None
    acceptance_criteria:str | None = None
    constraints:str | None = None
    priority:str | None = None
    confirmed:bool | None = None

class RequirementItemOut(BaseModel):
    id:int
    module:str
    feature:str
    description:str
    acceptance_criteria:str
    constraints:str
    priority:str
    sort_order:int
    confirmed:bool
    source_type:str = "requirement"
    source_ref_id:int|None =None

    model_config = {"from_attributes":True}

class ConfirmRequest(BaseModel):
    item_ids: list[int] | None = None

#--------------------------更新测试范围----------------
class TestScopeUpdate(BaseModel):
    test_scope:str = ""

# ----------------------------------------------------

class RequirementDocumentCreate(BaseModel):
    title:str
    content:str

class RequirementDocumentOut(BaseModel):
    id:int
    project_id:int
    title:str
    source_type:str
    status:str
    test_scope:str = ""
    created_at:datetime
    items:list[RequirementItemOut] =[]

    model_config = {"from_attributes":True}

class ConfirmRequest(BaseModel):
    item_ids:list[int] | None = None