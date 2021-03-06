from sqlalchemy import Column, Integer, String

from app.core.db import BaseModel as Base


class Auth(Base):
    __tablename__ = 'auth'
    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, nullable=False, comment='所属权限组id')
    name = Column(String(60), comment='权限字段')
    module = Column(String(50), comment='权限的模块')
