from app.database import Base
from sqlalchemy.orm import Mapped,mapped_column,relationship
from datetime import datetime
from sqlalchemy import String,Integer,Boolean,func,Text,ForeignKey,DateTime
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.project import Project

class KnowledgeDocument(Base):
    __tablename__="knowledge_documents"

    id:Mapped[int] = mapped_column(Integer,primary_key=True,autoincrement=True,comment="id")
    project_id:Mapped[int] = mapped_column(ForeignKey("projects.id"),nullable=False,comment="所属项目id")
    title:Mapped[str] = mapped_column(String(200),nullable=False,comment="文档标题")
    source_type:Mapped[str] = mapped_column(String(20),default="doc",comment="文档类型") # doc 业务文档 / case 历史用例 / defect 缺陷记录
    raw_content:Mapped[str] = mapped_column(Text,default="",comment="原始内容")
    status:Mapped[str] = mapped_column(String(20),default="processing",comment="状态") # processing / ready / failed
    error_message:Mapped[str] = mapped_column(Text,default="",comment="处理失败信息")
    chunk_count:Mapped[int] = mapped_column(Integer,default=0,comment="分块数量")
    vector_collection:Mapped[str] = mapped_column(String(120),default="",comment="向量集合名称")
    created_at:Mapped[datetime] = mapped_column(DateTime,server_default=func.now(),comment="创建时间")

    project:Mapped["Project"] = relationship(back_populates="knowledge_documents")
    chunks:Mapped[list["KnowledgeChunk"]] = relationship(back_populates="document",cascade="all,delete-orphan")

class KnowledgeChunk(Base):
    __tablename__ = "knowledge_chunks"

    id:Mapped[int] = mapped_column(Integer,primary_key=True,autoincrement=True,comment="id")
    document_id:Mapped[int] = mapped_column(ForeignKey("knowledge_documents.id"),nullable=False,comment="所属知识文档id")
    content:Mapped[str] = mapped_column(Text,nullable=False,comment="分块文本")
    heading:Mapped[str] = mapped_column(String(300),default="",comment="所属标题路径") # 所属标题路径，如「订单模块 > 退款规则」
    chroma_id:Mapped[str] = mapped_column(String(64),default="",comment="Chroma向量记录ID") # 向量库中对应记录的 id

    document:Mapped["KnowledgeDocument"] = relationship(back_populates="chunks")
