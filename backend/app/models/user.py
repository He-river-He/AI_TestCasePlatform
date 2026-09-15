from sqlalchemy import Boolean,DateTime,Integer,String,func
from app.database import Base
from sqlalchemy.orm import Mapped,mapped_column,relationship
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.project import Project
    from app.models.system_config import SystemConfig

class User(Base):
    __tablename__="users"
    id:Mapped[int]=mapped_column(Integer,primary_key=True,autoincrement=True,comment="id")
    username:Mapped[str]=mapped_column(String(64),unique=True,index=True,nullable=False,comment="用户名")
    password_hash:Mapped[str]=mapped_column(String(256),nullable=False,comment="密码哈希")
    is_admin:Mapped[bool]=mapped_column(Boolean,default=False,comment="是否管理员")
    is_active:Mapped[bool]=mapped_column(Boolean,default=True,comment="是否启动")
    create_at:Mapped[datetime]=mapped_column(DateTime,server_default=func.now(),comment="创建时间")

    projects:Mapped[list["Project"]] = relationship(back_populates="user")
    system_config:Mapped["SystemConfig"]=relationship(
        back_populates="user",
        cascade="all,delete-orphan",
        uselist=False,
    )