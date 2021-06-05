from sqlalchemy import Column, ForeignKey, SmallInteger, Integer, String, Float, Text

from app.core.db import EntityModel as Base


class Order(Base):
    '''用户订单'''
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_no = Column(String(20), unique=True, comment='订单号')
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False, comment='外键，用户id，注意并不是openid')  # 下单用户ID
    order_status = Column(SmallInteger, default=1, comment='订单状态 1:未支付 2:已支付 3:已发货 4:已支付，但库存不足 ')
    total_count = Column(Integer, comment='订单总量')
    total_price = Column(Float, comment='订单总价')
    prepay_id = Column(String(100), unique=True, comment='预支付id')

    def keys(self):
        self.append('create_time')
        return self.fields