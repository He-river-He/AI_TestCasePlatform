from app.database import Base
from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy import Boolean,String,Integer,func,DateTime,ForeignKey,Text,Index,text
from datetime import datetime

# 防止循环导入问题
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.requirement import RequirementDocument
    from app.models.generation import GenerationTask
    from app.models.testcase import TestCase
    from app.models.design import DesignAsset
    from app.models.knowledge import KnowledgeDocument

class Project(Base):
    __tablename__="projects"
    # 通过唯一索引保证每个用户最多有一个评测项目
    __table_args__=(
        Index(
            "uq_projects_user_eval",
            "user_id",
            unique=True,
            sqlite_where=text("is_eval=1"),
            postgresql_where=text("is_eval=true")
        ),
    )
    id:Mapped[int]=mapped_column(Integer,primary_key=True,autoincrement=True,comment="id")
    user_id:Mapped[int]=mapped_column(ForeignKey("users.id"),nullable=False,index=True,comment="项目所属用户")
    name:Mapped[str]=mapped_column(String(200),nullable=False,comment="项目名称")
    description:Mapped[str]=mapped_column(Text,default="",comment="项目描述")
    is_eval:Mapped[bool]=mapped_column(Boolean,default=False,comment="是否为评测项目")
    created_at:Mapped[datetime]=mapped_column(DateTime,server_default=func.now(),comment="创建时间")
    updated_at:Mapped[datetime]=mapped_column(DateTime,server_default=func.now(),onupdate=func.now(),comment="更新时间")

    user:Mapped["User"]=relationship(back_populates="projects")
    requirements:Mapped[list["RequirementDocument"]] = relationship(
        back_populates="project",
        cascade="all,delete-orphan",
    )
    generation_tasks:Mapped[list["GenerationTask"]] = relationship(
        back_populates="project",
        cascade="all,delete-orphan",
    )
    testcases:Mapped[list["TestCase"]] = relationship(
        back_populates="project",
        cascade="all,delete-orphan",
    )
    design_assets:Mapped[list["DesignAsset"]]= relationship(
        back_populates="project",
        cascade="all,delete-orphan",
    )
    knowledge_documents:Mapped[list["KnowledgeDocument"]] = relationship(
        back_populates="project",
        cascade="all,delete-orphan",
    )
