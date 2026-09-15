"""设计稿解析与合并：供 designs API 与 Agent 工具共用 """

from app.models.requirement import RequirementDocument,RequirementItem
from app.models.design import DesignAsset,DesignInsight
from sqlalchemy.orm import Session,joinedload
from fastapi import HTTPException
from app.services.design_storage import design_root
from pathlib import Path


def get_document(project_id:int,document_id:int,db:Session) -> RequirementDocument:
    doc = db.query(RequirementDocument).filter(
        RequirementDocument.project_id == project_id,
        RequirementDocument.id == document_id
    ).first()
    if not doc:
        raise HTTPException(404,"需求文档不存在")
    return doc

def get_asset(db:Session,project_id:int,asset_id:int) -> DesignAsset:
    asset = db.query(DesignAsset).options(joinedload(DesignAsset.insights)).filter(
        DesignAsset.project_id == project_id,
        DesignAsset.id == asset_id,
    ).first()
    if not asset:
        raise HTTPException(404,"设计稿不存在")
    return asset

def list_assets(db:Session,project_id:int,document_id:int) -> list[DesignAsset]:
    get_document(project_id,document_id,db)
    return (
        db.query(DesignAsset)
        .options(joinedload(DesignAsset.insights))
        .filter(DesignAsset.project_id == project_id , DesignAsset.document_id == document_id)
        .order_by(DesignAsset.created_at,DesignAsset.id)
        .all()
    )
# --------------------------------------------------------------------------------
def insight_to_dict(insight: DesignInsight) -> dict:
    return {
        "id": insight.id,
        "asset_id": insight.asset_id,
        "page": insight.page,
        "module": insight.module,
        "feature": insight.feature,
        "description": insight.description,
        "acceptance_criteria": insight.acceptance_criteria,
        "constraints": insight.constraints,
        "priority": insight.priority,
        "selected": insight.selected,
        "merged": insight.merged,
        "sort_order": insight.sort_order,
    }

def source_note(parse_source: str)->str:
    """把 parse_source 翻译成给用户看的来源说明。"""
    if not parse_source:
        return "来源未知（该解析结果早于来源标记功能，建议重新解析确认）"
    if parse_source == "mock":
        return "Mock 示例数据，未调用视觉模型；请先在「设置」页配置视觉模型再重新解析"
    if parse_source.startswith("vision:"):
        return f"由视角模型{parse_source.split(":",1)[1] or '(未记录模型名)'} 真实解析"
    return parse_source

def asset_to_summary(asset:DesignAsset) -> dict:
    insights = list(asset.insights or [])
    return {
        "id": asset.id,
        "document_id": asset.document_id,
        "asset_type": asset.asset_type,
        "title": asset.title,
        "filename": asset.filename,
        "figma_url": asset.figma_url,
        "status": asset.status,
        "error_message": asset.error_message,
        "parse_source": asset.parse_source or "",
        "is_mock_result": asset.parse_source == "mock",
        "source_note": source_note(asset.parse_source or ""),
        "is_design": asset.status != "not_design",
        "image_summary": asset.image_summary or "",
        "insight_count": len(insights),
        "unmerged_count": sum(1 for i in insights if not i.merged),
        "insights": [insight_to_dict(i) for i in insights],
    }

# ------------------------------------------------------------------------------
def safe_asset_path(asset:DesignAsset) -> Path:
    root = design_root()
    path = (root/asset.storage_path).resolve()
    if root not in path.parents:
        raise HTTPException(404,"设计稿文件不存在")
    return path

# ------------------------------------------------------------------------------

def feature_key(module:str,feature:str) -> tuple[str,str]:
    return (
        " ".join((module or "").lower().split()),
        " ".join((feature or "").lower().split()),
    )

def merge_insights(
    db:Session,
    project_id:int,
    document_id:int,
    insight_ids:list[int] | None = None,
    *,
    selected_only:bool=True
)->dict:
    """将未合并的设计功能点写入需求文档，并回退确认状态。"""
    document = get_document(project_id,document_id,db)
    query = (
        db.query(DesignInsight)
        .join(DesignAsset)
        .filter(
            DesignAsset.project_id == project_id,
            DesignAsset.document_id == document_id,
            DesignInsight.merged==False
        )
    )
    if insight_ids:
        query = query.filter(DesignInsight.id.in_(insight_ids))
    elif selected_only:
        query = query.filter(DesignInsight.selected == True) 
    insights = query.order_by(DesignAsset.id,DesignInsight.sort_order).all()

    existing_items = (
        db.query(RequirementItem)
        .filter(RequirementItem.document_id == document_id)
        .order_by(RequirementItem.sort_order)
        .all()
    )
    existing_key = {feature_key(item.module,item.feature) for item in existing_items}
    next_order = max((item.sort_order for item in existing_items),default=-1)+1
    added = 0

    for insight in insights:
        key = feature_key(insight.module,insight.feature)
        if key not in existing_key:
            db.add(RequirementItem(
                document_id=document_id,
                module=insight.module,
                feature=insight.feature,
                description=insight.description,
                acceptance_criteria=insight.acceptance_criteria,
                constraints=insight.constraints,
                priority=insight.priority,
                sort_order=next_order,
                confirmed=False,
                source_type="design",
                source_ref_id=insight.asset_id,
            ))
            next_order +=1
            existing_key.add(key)
            added+=1
        insight.merged = True

    if insights:
        document.status = "structured"
        db.query(RequirementItem).filter(
            RequirementItem.document_id == document_id
        ).update({"confirmed":False},synchronize_session=False)
    db.commit()
    refreshed = (
        db.query(RequirementDocument)
        .options(joinedload(RequirementDocument.items))
        .filter(RequirementDocument.id == document_id)
        .first()
    )
    return {
        "document":refreshed,
        "merged_count":len(insights),
        "added_count":added,
        "document_status":refreshed.status if refreshed else document.status,
        "item_count":len(refreshed.items) if refreshed else 0
    }
