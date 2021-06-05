from sqlalchemy import Column, Integer, ForeignKey

from app.core.db import BaseModel as Model, db


class Product2Image(Model):
    __tablename__ = 'product_image'
    product_id = Column(Integer, ForeignKey('product.id'), primary_key=True, comment='外键, 商品id')
    img_id = Column(Integer, ForeignKey('image.id'), primary_key=True, comment='外键，关联图片表')
    order = Column(Integer, nullable=False, comment='图片排序序号')
