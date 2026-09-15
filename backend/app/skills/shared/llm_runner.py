# 建立 Skill 层和 app.ai.chains 之间的轻量适配器
from app.ai.chains import generate_cases
from app.services.settings_service import RuntimeModelConfig

async def call_for_cases(
    system_prompt:str,
    user_prompt:str,
    skill_name:str,
    config:RuntimeModelConfig
)->list[dict]:
    return await generate_cases(system_prompt,user_prompt,skill_name,config)