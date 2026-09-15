from app.skills.base import SkillContext
from app.skills.shared.prompt_loader import load_prompt
from app.skills.shared.mock import MOCK_SOURCE,MOCK_DESIGN_INSIGHTS
from app.ai.chains import parse_design_image

SKILL_DIR = __import__("pathlib").Path(__file__).resolve().parent

async def run(inputs:dict,context:SkillContext) -> dict:
    """返回 insights / source / is_design / image_summary，供上层如实处理。"""
    if context.use_mock:
        return {
            "insights":MOCK_DESIGN_INSIGHTS,
            "source":MOCK_SOURCE,
            "is_design":True,
            "image_summary":"",
        }
    system_prompt = load_prompt(SKILL_DIR,"prompt.md")
    result = await parse_design_image(
        system_prompt,
        inputs["image_data"],
        inputs["content_type"],
        context.model_config,
    )
    return {
        "insights":result.get("features") or [],
        "source":f"vision:{context.model_config.vision_model}",
        "is_design":bool(result.get("is_design",True)),
        "image_summary":result.get("image_summary") or "",
    }
