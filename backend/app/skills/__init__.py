from app.skills.base import SkillContext
from app.skills.registry import get_registry
from app.services.settings_service import RuntimeModelConfig,get_project_runtime_config
from app.services.design_service import get_asset,safe_asset_path
from sqlalchemy.orm import Session
from app.models.design import DesignAsset,DesignInsight
from fastapi import HTTPException

__all__ = [
    "SkillContext",
    "get_registry",
    "parse_requirements",
    "parse_asset",
    "propose_test_scope",
    "generate_cases_for_feature",
    "generate_specialist_cases",
]

def _build_context(model_config:RuntimeModelConfig,**kwargs) -> SkillContext:
    return SkillContext(model_config=model_config,use_mock=model_config.use_mock_llm,**kwargs)

async def parse_requirements(raw_content:str,model_config:RuntimeModelConfig) -> list[dict]:
    registry = get_registry()
    result = await registry.run(
        name="requirement_parser",
        inputs={"raw_content":raw_content},
        context=_build_context(model_config),
    )

    return result.get("items",[])

async def parse_asset(db:Session,project_id:int,asset_id:int) -> DesignAsset:
    """解析图片设计稿，写入 DesignInsight；Figma 链接不可直接解析。

    视觉解析与生成模型 Mock 解耦：已配置视觉模型时一律真实调用；
    仅未配置视觉且开启 LLM Mock 时才返回示例数据，并写入 parse_source 供上层展示。
    """
    asset = get_asset(db,project_id,asset_id)
    if asset.asset_type != "image":
        raise HTTPException(400,"Figma 链接首版不支持自动解析，请上传对应页面截图")
    path = safe_asset_path(asset)
    if not path.is_file():
        raise HTTPException(404,"设计稿文件不存在")
    
    config = get_project_runtime_config(db,project_id)
    use_mock = not config.vision_configured and config.use_mock_llm
    if not config.vision_configured and not config.use_mock_llm:
        raise HTTPException(400, "尚未配置视觉模型，请先到「设置」页完成配置")
    
    asset.status = "parsing"
    asset.error_message = ""
    asset.parse_source=""
    asset.image_summary=""
    db.commit()

    try:
        result = await get_registry().run(
            "design_parser",
            {"image_data":path.read_bytes(),"content_type":asset.content_type},
            SkillContext(
                model_config=config,
                project_id=project_id,
                use_mock=use_mock
            ),
        )
        insights_data = result.get("insights") or []
        parse_source = str(result.get("source") or ("mock" if use_mock else ""))[:120]
        is_design = bool(result.get("is_design",True))
        image_summary= str(result.get("image_summary") or "")[:1000]
        db.query(DesignInsight).filter_by(DesignInsight.asset_id == asset.id).delete()
        # 非设计稿:不写功能点,标记not_design,有上层友好提示
        if not is_design:
            asset.status = "not_design"
            asset.parse_source = parse_source
            asset.image_summary = image_summary
            db.commit()
            return get_asset(db,project_id,asset_id)
        for index,item in enumerate(insights_data):
            db.add(DesignInsight(
                asset_id=asset_id,
                page=str(item.get("page",""))[:200],
                module=str(item.get("module",""))[:100],
                feature=str(item.get("feature",""))[:200] or f"设计功能点{index +1}",
                description=str(item.get("description","")),
                acceptance_criteria=str(item.get("acceptance_criteria","")),
                constraints=str(item.get("constraints","")),
                priority=item.get("priority") if item.get("priority") in {"P0","P1","P2"} else "P1",
                sort_order=index,
                selected=True,
            ))
            asset.status = "parsed"
            asset.parse_source=parse_source
            asset.image_summary= image_summary
            db.commit()
    except HTTPException:
        raise
    except Exception as exc:
        db.rollback()
        failed_asset = db.get(DesignAsset,asset_id)
        if failed_asset:
            failed_asset.status = "failed"
            failed_asset.error_message = str(exc)[:1000]
            failed_asset.parse_source = ""
            db.commit()
        raise HTTPException(502,f"设计稿解析失败:{str(exc)[:300]}") from exc
    return get_asset(db,project_id,asset_id)

async def propose_test_scope(raw_content:str,model_config:RuntimeModelConfig)->dict:
    registry = get_registry()
    result = await registry.run(
        "test_proposal",
        {"raw_content":raw_content},
        _build_context(model_config)
    )
    return result.get("scope",[])

# -------------------------------------------------------------------------
async def generate_cases_for_feature(
    feature_item:dict,
    model_config:RuntimeModelConfig,
    strategy:str = "detailed"
) -> list[dict]:
    registry = get_registry()
    strategy = registry.normalize_strategy(strategy)
    result = await registry.run(
        name="case_writer",
        inputs={"feature_item":feature_item,"strategy":strategy},
        context=_build_context(model_config,strategy=strategy)
    )
    return result.get("cases",[])

async def generate_specialist_cases(
    feature_item:dict,
    skill_name,
    model_config:RuntimeModelConfig,
) -> list[dict]:
    registry = get_registry()
    resolved = registry.reslove_skill_name(skill_name)
    result = await registry.run(
        resolved,
        {"feature_item":feature_item},
        _build_context(model_config),
    )
    return result.get("cases",[])
    