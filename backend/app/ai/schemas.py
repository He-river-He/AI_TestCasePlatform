""" 定义模型的输出结构 """
from pydantic import BaseModel,ConfigDict,RootModel,Field,field_validator
import json
from typing import Any


# 需求功能点结构
class RequirementFeature(BaseModel):
    model_config = ConfigDict(extra="ignore")

    module: str = ""
    feature: str = ""
    description: str = ""
    acceptance_criteria: str = ""
    constraints: str = ""
    priority: str = "P1"
# 需求功能点列表结构
class RequirementFeatureBatch(RootModel[list[RequirementFeature]]):
    pass

# 设计稿功能点结构
class DesignFeature(BaseModel):
    model_config = ConfigDict(extra="ignore")

    page: str =""
    module: str = ""
    feature: str = ""
    description: str = ""
    acceptance_criteria: str = ""
    constraints: str = ""
    priority: str = "P1"

# 设计稿功能点列表结构
class DesignFeatureBatch(RootModel[list[DesignFeature]]):
    pass

class DesignParseResult(BaseModel):
    """视觉解析结果：先判定是否产品设计稿，再给出功能点。"""
    model_config=ConfigDict(extra="ignore")

    is_design: bool = True
    image_summary: str ="" #对图片内容的一句话客观描述
    features: list[DesignFeature] = Field(default_factory=list)


# -------------------------------------------------------------------------------
# 测试用例结构
class GeneratedTestCase(BaseModel):
    model_config = ConfigDict(extra="ignore")

    title: str = ""
    priority: str = "P2"
    case_type: str = "functional"
    is_smoke: bool = False
    precondition: str = ""
    steps: list[str] = Field(default_factory=list)
    expected_result: str = ""

    @field_validator("steps", mode="before")
    @classmethod
    def normalize_steps(cls, value: Any) -> list[str]:
        if isinstance(value, list):
            return [str(item) for item in value]
        if isinstance(value, str):
            text = value.strip()
            if not text:
                return []
            try:
                parsed = json.loads(text)
            except json.JSONDecodeError:
                return [line.strip() for line in text.splitlines() if line.strip()]
            if isinstance(parsed, list):
                return [str(item) for item in parsed]
            return [str(parsed)]
        return []
    
# 测试用例列表结构
class GeneratedCaseBatch(RootModel[list[GeneratedTestCase]]):
    pass

# ----------------------------------------------------------------------
# 测试方案结构
class TestProposal(BaseModel):
    model_config = ConfigDict(extra="ignore")

    in_scope:list[str] = Field(default_factory=list)
    out_scope:list[str] = Field(default_factory=list)
    risks:list[str] = Field(default_factory=list)

# ----------------------------------------------------------------------
# 用例评测
class CaseJudgement(BaseModel):
    model_config = ConfigDict(extra="ignore")

    index: int
    relevance: int =3
    executability: int = 3
    verifiability: int = 3
    hallucination: bool = False
    hallucination_reason: str = ""
    comment: str = ""

class CaseJudgementBatch(BaseModel):
    model_config = ConfigDict(extra="ignore")

    judgements: list[CaseJudgement] = Field(default_factory=list)

# AI 判定哪些标准测试点被生成用例覆盖
class CoverageDecision(BaseModel):
    model_config = ConfigDict(extra="ignore")
    covered_indexes:list[int] = Field(default_factory=list)