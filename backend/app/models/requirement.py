from app.database import Base
from sqlalchemy import String,Boolean,Integer,ForeignKey,Text,func,DateTime
from sqlalchemy.orm import Mapped,mapped_column,relationship
from datetime import datetime
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.project import Project
    from app.models.design import DesignAsset

#  需求文档本体
class RequirementDocument(Base):
    __tablename__="requirement_documents"
    id:Mapped[int]=mapped_column(Integer,primary_key=True,autoincrement=True,comment="id")
    project_id:Mapped[int]=mapped_column(ForeignKey("projects.id"),comment="project_id")
    title:Mapped[str]=mapped_column(String(200),nullable=False,comment="需求文档标题")
    source_type:Mapped[str]=mapped_column(String(20),default="text",comment="来源类型")
    raw_content:Mapped[str]=mapped_column(Text,default="",comment="原始需求内容")
    test_scope:Mapped[str]=mapped_column(Text,default="",comment="测试范围")
    status:Mapped[str]=mapped_column(String(20),default="uploaded",comment="文档状态")
    is_eval:Mapped[bool]=mapped_column(Boolean,default=False,comment="是否为评测文档")
    created_at:Mapped[datetime]=mapped_column(DateTime,server_default=func.now(),comment="创建时间")

    project:Mapped["Project"]=relationship(back_populates="requirements")
    items:Mapped[list["RequirementItem"]]=relationship(back_populates="document",cascade="all,delete-orphan")
    design_assets:Mapped[list["DesignAsset"]]=relationship(
        back_populates="document",
        cascade="all,delete-orphan",
    )



# 从需求中拆出来的功能点
class RequirementItem(Base):
    __tablename__="requirement_items"
    id:Mapped[int]=mapped_column(Integer,primary_key=True,autoincrement=True,comment="id")
    document_id:Mapped[int]=mapped_column(ForeignKey("requirement_documents.id"),nullable=False,comment="document_id")
    module:Mapped[str]=mapped_column(String(100),default="",comment="模块名")
    feature:Mapped[str]=mapped_column(String(200),nullable=False,comment="功能点")
    description:Mapped[str]=mapped_column(Text,default="",comment="功能描述")
    acceptance_criteria:Mapped[str]=mapped_column(Text,default="",comment="验收标准")
    constraints:Mapped[str]=mapped_column(Text,default="",comment="约束条件")
    priority:Mapped[str]=mapped_column(String(10),default="p1",comment="优先级")
    sort_order:Mapped[int]=mapped_column(Integer,default=0,comment="排序号")
    confirmed:Mapped[bool]=mapped_column(Boolean,default=False,comment="是否已确认")
    source_type:Mapped[str]=mapped_column(String(20),default="requirement",comment="来源类型")
    source_ref_id:Mapped[int | None]=mapped_column(Integer,comment="来源记录ID")
    
    document:Mapped["RequirementDocument"]=relationship(back_populates="items")