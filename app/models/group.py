from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.core.auth import get_ep_id
from app.core.db import BaseModel as Base, db
from app.models.auth import Auth


class Group(Base):
    __tablename__ = 'group'
    id = Column(Integer, primary_key=True)
    name = Column(String(60), unique=True, comment='权限组名称')
    info = Column(String(255), comment='权限组描述')

    @property
    def auth_list(self):
        # 权限列表中的每一项包含权限名（权限字段名）和权限模块
        auth_list = db.session.query(Auth.name, Auth.module).filter_by(group_id=self.id).all()
        auth_list = [{'id': get_ep_id(auth[0]), 'name':auth[0], 'module': auth[1]} for auth in auth_list]