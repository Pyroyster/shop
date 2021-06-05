from sqlalchemy import Column, Integer, String, SmallInteger

from app.core.db import EntityModel as Base
from app.libs.enums import UrlFromEnum


class Image(Base):
    __tablename__ = 'image'
    id = Column(Integer, primary_key=True, autoincrement=True)
    _url = Column('url', String(255), comment='图片路径')
    _from = Column('from', SmallInteger, default=UrlFromEnum.LOCAL.value, comment='图片来源: 1 本地，2 公网')

    def __repr__(self):
        return f'<Image(id={self.id}, url={self._url}>'

    def keys(self):
        self.hide('id', '_url', '_from').append('url')
    
    @property
    def url(self):
        return self.get_url(self._url)

    @staticmethod
    def get_img_by_id(id):
        return Image.query.filter_by(id=id).first_or_404()
