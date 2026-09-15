from app.database import Base
from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy import Integer,Boolean,String,func,DateTime,ForeignKey,Text
from datetime import datetime
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.project import Project

class TestCase(Base):
    __tablename__ = "testcases"

    id:Mapped[int] = mapped_column(Integer,primary_key=True,autoincrement=True,comment="id")
    project_id:Mapped[int]=mapped_column(ForeignKey("projects.id"),comment="project_id")
    draft_id:Mapped[int]=mapped_column(ForeignKey("generated_case_drafts.id"),comment="draft_id")
    requirement_item_id:Mapped[int]=mapped_column(ForeignKey("requirement_items.id"),comment="requirement_item_id")
    title:Mapped[str]=mapped_column(String(500),nullable=False,comment="测试用例标题")
    priority:Mapped[str]=mapped_column(String(10),default="P2",comment="优先级")
    case_type:Mapped[str]=mapped_column(String(20),default="functional",comment="用例类型")
    is_smoke:Mapped[bool]=mapped_column(Boolean,default=False,comment="是否冒烟用例")
    precondition:Mapped[str]=mapped_column(Text,default="",comment="前置条件")
    steps:Mapped[str]=mapped_column(Text,default="",comment="测试步骤")
    expected_result:Mapped[str]=mapped_column(Text,default="",comment="预期结果")
    status:Mapped[str]=mapped_column(String(20),default="active",comment="用例状态")
    source:Mapped[str]=mapped_column(String(20),default="ai_generated",comment="用例来源")
    created_at:Mapped[datetime]=mapped_column(DateTime,server_default=func.now(),comment="创建时间")
    updated_at:Mapped[datetime]=mapped_column(DateTime,server_default=func.now(),onupdate=func.now(),comment="更新时间")

    project:Mapped["Project"] = relationship(back_populates="testcases")