from datetime import datetime
from sqlalchemy import String,Integer,Boolean,DateTime,func,ForeignKey,Text,Float
from sqlalchemy.orm import relationship,Mapped,mapped_column
from app.database import Base
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.project import Project
    from app.models.requirement import RequirementItem

class GenerationTask(Base):
    __tablename__="generation_tasks"

    id:Mapped[int]=mapped_column(Integer,primary_key=True,autoincrement=True,comment="id")
    project_id:Mapped[int]=mapped_column(ForeignKey("projects.id"),nullable=False,comment="所属项目id")
    document_id:Mapped[int]=mapped_column(ForeignKey("requirement_documents.id"),nullable=False,comment="需求文档id")
    strategy:Mapped[str]=mapped_column(String(50),default="full",comment="生成策略")
    strategy_config:Mapped[str]=mapped_column(Text,default="",comment="策略配置")
    status:Mapped[str]=mapped_column(String(20),default="pending",comment="任务状态")
    progress:Mapped[int]=mapped_column(Integer,default=0,comment="任务进度百分比")
    stage:Mapped[str]=mapped_column(String(100),default="",comment="当前执行阶段描述")
    error_message:Mapped[str]=mapped_column(Text,default="",comment="任务失败时的错误信息")
    tokens_used:Mapped[int]=mapped_column(Integer,default=0,comment="已使用的token数量")
    is_eval:Mapped[bool]=mapped_column(Boolean,default=False,comment="是否为评测项目")
    knowledge_refs: Mapped[str] = mapped_column(Text,default="") # JSON: {item_id: [{title, heading, score}]}，RAG 溯源
    pause_requested:Mapped[bool]=mapped_column(Boolean,default=False) #协作式暂停:当前节点结束后生效
    run_lease:Mapped[str] = mapped_column(String(64),default="") #运行租约，防止并发执行
    run_started_at: Mapped[datetime | None] = mapped_column(DateTime,nullable=True)
    created_at:Mapped[datetime]=mapped_column(DateTime,server_default=func.now(),comment="创建时间")
    updated_at:Mapped[datetime]=mapped_column(DateTime,server_default=func.now(),onupdate=func.now(),comment="更新时间")

    project:Mapped["Project"] = relationship(back_populates="generation_tasks")
    drafts:Mapped[list["GeneratedCaseDraft"]]=relationship(
        back_populates="task",
        cascade="all,delete-orphan",
    )
    quality_report:Mapped["QualityReport | None"]=relationship(
        back_populates="task",
        uselist=False,
        cascade="all,delete-orphan",
    )
    @property
    def review_stats(self)->dict:
        """从 drafts 实时汇总评审信号：采纳率 / 编辑率 / 驳回率。"""
        drafts = self.drafts or []
        total=len(drafts)
        adopted=sum(1 for d in drafts if d.review_status == "adopted")
        rejected=sum(1 for d in drafts if d.review_status == "rejected")
        edited_adopted = sum(1 for d in drafts if d.review_status == "adopted" and d.was_edited)
        reviewed = adopted+rejected

        def rate(part:int,whole:int) -> float:
            return round(part/whole*100,1) if whole else 0.0
        return {
            "total": total,
            "adopted": adopted,
            "rejected": rejected,
            "edited_adopted": edited_adopted,
            "pending": total - reviewed,
            "reviewed": reviewed > 0,
            "adoption_rate": rate(adopted, total),
            "edit_rate": rate(edited_adopted, adopted),
            "rejection_rate": rate(rejected, total),
        }



# 保存 AI 生成的候选用例
class GeneratedCaseDraft(Base):
    __tablename__="generated_case_drafts"

    id:Mapped[int]=mapped_column(Integer,primary_key=True,autoincrement=True,comment="id")
    task_id:Mapped[int]=mapped_column(ForeignKey("generation_tasks.id"),nullable=False,comment="所属生成任务id")
    requirement_item_id:Mapped[int | None]=mapped_column(ForeignKey("requirement_items.id"),comment="关联功能点id")
    title:Mapped[str]=mapped_column(String(500),nullable=False,comment="用例标题")
    priority:Mapped[str]=mapped_column(String(10),default="P2",comment="优先级")
    case_type:Mapped[str]=mapped_column(String(20),default="functional",comment="用例类型")
    precondition:Mapped[str]=mapped_column(Text,default="",comment="前置条件")
    steps:Mapped[str]=mapped_column(Text,default="",comment="步骤内容")
    expected_result:Mapped[str]=mapped_column(Text,default="",comment="预期结果")
    quality_status:Mapped[str]=mapped_column(String(20),default="pending",comment="质检结果")
    quality_issues:Mapped[str]=mapped_column(Text,default="",comment="质检问题")
    review_status:Mapped[str]=mapped_column(String(20),default="pending",comment="评审状态")
    was_edited:Mapped[bool]=mapped_column(Boolean,default=False,comment="是否被人工编辑过")
    reject_reason:Mapped[str]=mapped_column(String(200),default="",comment="驳回原因")
    is_smoke:Mapped[bool]=mapped_column(Boolean,default=False,comment="是否冒烟用例")
    skill_name:Mapped[str]=mapped_column(String(50),default="")
    generation_key:Mapped[str | None]=mapped_column(String(160),nullable=True,unique=True)
    judge_score:Mapped[float | None]=mapped_column(Float,nullable=True,comment="AI评分")
    judge_issues:Mapped[str]=mapped_column(Text,default="",comment="AI评分细节")

    task:Mapped["GenerationTask"]=relationship(back_populates="drafts")
    requirement_item:Mapped["RequirementItem | None"] = relationship()

    @property
    def module(self) -> str:
        return self.requirement_item.module if self.requirement_item else ""
    
    @property
    def feature(self) -> str:
        return self.requirement_item.feature if self.requirement_item else ""
    

# 保存生成结果的质量统计
class QualityReport(Base):
    __tablename__="quality_reports"

    id:Mapped[int]=mapped_column(Integer,primary_key=True,autoincrement=True,comment="id")
    task_id:Mapped[int]=mapped_column(ForeignKey("generation_tasks.id"),nullable=False,unique=True,comment="所属生成任务id")
    total_cases:Mapped[int]=mapped_column(Integer,default=0,comment="总用例数")
    pass_count:Mapped[int]=mapped_column(Integer,default=0,comment="通过数")
    warning_count:Mapped[int]=mapped_column(Integer,default=0,comment="警告数")
    fail_count:Mapped[int]=mapped_column(Integer,default=0,comment="失败数")
    coverage_rate:Mapped[float]=mapped_column(Float,default=0.0,comment="覆盖率")
    uncovered_features:Mapped[str]=mapped_column(Text,default="",comment="未覆盖功能点")
    suggestions:Mapped[str]=mapped_column(Text,default="",comment="质检建议")
    avg_judge_score:Mapped[float | None]=mapped_column(Float,nullable=True,comment="平均AI评分")
    hallucination_count:Mapped[int]=mapped_column(Integer,default=0,comment="疑似幻觉数")
    duplicate_count:Mapped[int]=mapped_column(Integer,default=0,comment="重复数")
    created_at:Mapped[datetime]=mapped_column(DateTime,server_default=func.now(),comment="创建时间")

    task:Mapped["GenerationTask"]=relationship(back_populates="quality_report")