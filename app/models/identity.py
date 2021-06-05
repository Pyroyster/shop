from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, ForeignKey, SmallInteger, Integer, String
from flask import current_app

from app.core.db import EntityModel as Base, db
from app.libs.enums import ClientTypeEnum


class Identity(Base):  # Base继承了db.Model
    __tablename__ = 'identity'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False, comment='外键，用户id')  # 用户ID
    type = Column(Integer, nullable=False, comment='登录类型')
    identifier = Column(String(100), unique=True, comment='标识(手机号、邮箱、用户名或第三方应用的唯一标识)')
    _credential = Column('credential', String(100), comment='密码凭证(站内的保存密码，站外的不保存或保存token)')
    verified = Column(SmallInteger, default=0, comment='是否已经验证: 0未验证, 1已验证')

    def keys(self):
        self.hide('id', 'user_id', '_credential')
        self.append('name')
        return self.fields

    # 登录类型名
    @property
    def name(self):
        return ClientTypeEnum(self.type).name.lower()

    @property
    def credential(self):
        return self._credential

    @credential.setter
    def credential(self, raw):
        self._credential = raw

    @property
    def password(self):
        return self._credential

    @password.setter
    # 站内登录方式(用户名、手机、邮箱)的密码需要加密
    def set_password(self, raw):
        if ClientTypeEnum(self.type) in current_app.config['CLINET_INNER_TYPES']:
            self._credential = generate_password_hash(raw)
        # 第三方应用的token
        else:
            self._credential = raw

    # 校验站内登录方式(用户名、手机、邮箱)
    def validate_password(self, password, e=None):
        if not self._credential:
            return False
        is_validate = check_password_hash(self._credential, password)
        if not is_validate and e:
            raise e
        return is_validate

    """
        def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

    """

