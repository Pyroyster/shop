from sqlalchemy import Column, Integer, Float, String, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship, backref

from app.core.db import EntityModel as Base, db
from app.models.m2m import Product2Image


class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True, autoincrement=True)
    category_id = Column(Integer, comment='所属类别组id')
    name = Column(String(50), comment='商品名称')
    price = Column(Float, comment='价格(单位:分)')
    stock = Column(Integer, comment='库存量')
    main_img_url = Column(String(255))
    _from = Column('from', SmallInteger, default=1)
    _images = Column('image', secondary='product_image', order_by=Product2Image.order.asc(), backref=backref('product', lazy='dynamic'))

    @property
    def main_image(self):
        return self.get_url(self.main_img_url)

    @property
    def images(self):
        _images = self._images
        return [item.url for item in _images]