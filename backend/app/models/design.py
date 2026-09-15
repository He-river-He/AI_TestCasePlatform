from app.database import Base
from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy import Integer,ForeignKey,String,Text,DateTime,func
from datetime import datetime
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.project import Project
    from app.models.requirement import RequirementDocument

# 设计稿资源表
class DesignAsset(Base):
    __tablename__ = "design_assets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True,comment="id")
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False, index=True,comment="project_id")
    document_id: Mapped[int] = mapped_column(
        ForeignKey("requirement_documents.id"), nullable=False, index=True,comment="document_id"
    )
    asset_type: Mapped[str] = mapped_column(String(20), nullable=False,comment="资源类型")  # image / figma
    title: Mapped[str] = mapped_column(String(200), default="",comment="标题")
    filename: Mapped[str] = mapped_column(String(255), default="",comment="文件名")
    content_type: Mapped[str] = mapped_column(String(100), default="",comment="文件MIME类型") #image/png image/jpeg
    storage_path: Mapped[str] = mapped_column(String(500), default="",comment="存储路径")
    figma_url: Mapped[str] = mapped_column(String(1000), default="",comment="Figma 设计稿的访问地址")
    status: Mapped[str] = mapped_column(String(20), default="uploaded",comment="处理状态")
    error_message: Mapped[str] = mapped_column(Text, default="",comment="错误信息")
    # 解析结果来源：mock 或 vision:{模型名}，用于区分示例数据与真实视觉模型输出
    parse_source: Mapped[str] = mapped_column(String(120), default="",comment="解析结果来源")
    # 视觉模型对图片内容的客观描述；非设计稿时用于友好提示
    image_summary: Mapped[str] = mapped_column(Text, default="",comment="视觉模型对图片内容的总结")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(),comment="创建时间")

    project:Mapped["Project"] = relationship(back_populates="design_assets")
    document:Mapped["RequirementDocument"]=relationship(back_populates="design_assets")
    insights:Mapped[list["DesignInsight"]]=relationship(
        back_populates="assets",
        cascade="all,delete-orphan",
        order_by="DesignInsight.sort_order",
    )


class DesignInsight(Base):
    __tablename__ = "design_insights"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    asset_id: Mapped[int] = mapped_column(ForeignKey("design_assets.id"), nullable=False, index=True)
    page: Mapped[str] = mapped_column(String(200), default="")
    module: Mapped[str] = mapped_column(String(100), default="")
    feature: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, default="")
    acceptance_criteria: Mapped[str] = mapped_column(Text, default="",comment="验收标准")
    constraints: Mapped[str] = mapped_column(Text, default="",comment="约束条件")
    priority: Mapped[str] = mapped_column(String(10), default="P1")
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    selected: Mapped[bool] = mapped_column(default=True)
    merged: Mapped[bool] = mapped_column(default=False)

    assets:Mapped["DesignAsset"] = relationship(back_populates="insights")