from pathlib import Path

from app.skills.shared.mock import mock_cases
from app.skills.base import SkillContext
from app.skills.shared.prompt_loader import load_prompt
from app.skills.shared.prompt_formatter import feature_to_user_prompt
from app.skills.shared.llm_runner import call_for_cases

# 获取当前文件的路径
SKILL_DIR = Path(__file__).resolve().parent
SKILL_NAME = "case_writer"
PROMPT_PATH = "prompts/write.md"

QUICK_SUFFIX = (
    "\n\n【本次仅生成冒烟用例】只输出核心主路径用例,每个功能点2~4条"
    "全部 is_smoke=true,优先 P0/P1,case_type 以functional为主,可含1条关键异常"
)

async def run(
    inputs:dict,
    context:SkillContext
) -> dict:
    feature_item = inputs["feature_item"]
    scope = inputs.get("scope")
    knowledge= inputs.get("knowledge")
    strategy = inputs.get("strategy","full")
    quick = strategy == "quick"
    if context.use_mock:
        if quick:
            cases = mock_cases(
                feature_item["feature"],3,
                ["functional","functional","exception"],SKILL_NAME,smoke=True
            )
        else:
            cases = mock_cases(
                feature_item["feature"],6,
                ["functional","boundary","exception"],SKILL_NAME,
            )
        return {"cases":cases}
    system_prompt = load_prompt(SKILL_DIR,PROMPT_PATH)
    if quick:
        system_prompt = system_prompt + QUICK_SUFFIX
    user_prompt = feature_to_user_prompt(feature_item,scope,knowledge)
    cases = await call_for_cases(system_prompt,user_prompt,SKILL_NAME,context.model_config)
    return {"cases":cases}
    

    