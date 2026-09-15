from app.skills.shared.mock import MOCK_SCOPE
from pathlib import Path
from app.skills.base import SkillContext
from app.skills.shared.prompt_loader import load_prompt
from app.ai.chains import generate_test_proposal
from langchain_core.exceptions import OutputParserException

SKILL_DIR = Path(__file__).resolve().parent

def _normalize(data) -> dict:
    if not isinstance(data,dict):
        return {}
    return {
        "in_scope":list(data.get("in_scope") or []),
        "out_scope":list(data.get("out_scope") or []),
        "risks":list(data.get("risks") or []),
    }

async def run(inputs:dict,context:SkillContext)->dict:
    if context.use_mock:
        return {"scope":MOCK_SCOPE}
    
    raw_content = inputs["raw_content"]
    system_prompt = load_prompt(SKILL_DIR,"prompt.md")
    try:
        data=await generate_test_proposal(system_prompt,raw_content,context.model_config)
    except OutputParserException:
        data={}
    return {"scope":_normalize(data)}
