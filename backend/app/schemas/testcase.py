from pydantic import BaseModel,Field, model_validator
from datetime import datetime
from typing import Literal

class TestCaseUpdate(BaseModel):
    title: str | None = None
    priority: str | None = None
    case_type: str | None = None
    precondition: str | None = None
    steps: str | None = None
    expected_result: str | None = None
    module: str | None = None
    feature: str | None = None

class TestCaseOut(BaseModel):
    id: int
    project_id: int
    requirement_item_id: int | None = None
    project_name: str = ""
    title: str
    priority: str
    case_type: str
    is_smoke: bool = False
    precondition: str
    steps: str
    expected_result: str
    status: str
    source: str
    created_at: datetime
    module: str = ""
    feature: str = ""

    model_config = {"from_attributes": True}

class CatalogRename(BaseModel):
    type: Literal["module","feature"]
    old_module: str = Field(...,min_length=1)
    old_feature: str | None = None
    new_name:str = Field(...,min_length=1,max_length=200)

    @model_validator(mode="after")
    def validate_feature_rename(self):
        if self.type == "feature" and not self.old_feature:
            raise ValueError("重命名功能点需提供old_feature")
        return self
    
class CatalogRenameOut(BaseModel):
    updated_items:int