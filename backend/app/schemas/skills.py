from pydantic import BaseModel

class SkillOut(BaseModel):
    name:str
    version:str
    title:str
    description:str
    category:str
    stage:str
    tags:list[str] = []
    selectable:bool = False
    group: str | None = None
    icon: str | None = None

class StrategyOut(BaseModel):
    key:str
    title:str
    description:str = ""
    min_cases_per_feature:int =2
    max_cases_per_feature:int =4
    recommended:bool = False

class SkillCatalogOut(BaseModel):
    core: list[SkillOut] = []
    specialist: list[SkillOut] = []
    strategies: list[StrategyOut] = []
