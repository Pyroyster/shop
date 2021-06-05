from wtforms import BooleanField, StringField, IntegerField, PasswordField, FileField, FieldList
from wtforms.validators import DataRequired, ValidationError, length, Email, Regexp, EqualTo, Optional, NumberRange

from app.libs.enums import ClientTypeEnum
from app.core.validator import BaseValidator

########## 基础公用的参数校验器 ##########
# id必须为正整数
class IDMustBePositiveIntValidator(BaseValidator):
    id = IntegerField(validators=[DataRequired()])

    def validate_id(self, value):
        id = value.data
        if not self.isPositiveInteger(id):
            raise ValidationError(message='ID 必须为正整数')
        self.id.data = int(id)


# id必须为非负整数
class IDMustBeNaturalNumValidator(BaseValidator):
    id = IntegerField(validators=[DataRequired()])

    def validate_id(self, value):
        id = value.data
        if not self.isNaturalNumber(id):
            raise ValidationError(message='ID 必须为非负整数')
        self.id.data = int(id)

class PaginateValidator(BaseValidator):
    page = IntegerField('当前页数', validators=[NumberRange(min=1)], default=1)  # 当前页
    size = IntegerField('每页条数', validators=[NumberRange(min=1, max=100)], default=10)  # 每页条目个数

    def validate_page(self, value):
        self.page.data = int(value.data)

    def validate_size(self, value):
        self.size.data = int(value.data)

class ClientValidator(BaseValidator):
    account = StringField(validators=[DataRequired(message='账户不为空'),
                                      length(min=4, max=32)])
    secret = StringField()
    type = IntegerField(validators=[DataRequired()])

    def validate_type(self, value):
        try:
            client = ClientTypeEnum(value.data)
        except ValueError as e:
            raise e
        self.type.data = client


class TokenValidator(BaseValidator):
    token = StringField(validators=[DataRequired()])

# 注册时，密码校验
class CreatePasswordValidator(BaseValidator):
    password = PasswordField('新密码', validators=[
        DataRequired(message='新密码不可为空'),
        Regexp(r'^[A-Za-z0-9_*&$#@]{6,22}$', message='密码长度必须在6~22位之间，包含字符、数字和 _ '),
        EqualTo('confirm_password', message='两次输入的密码不一致，请输入相同的密码')
    ])
    confirm_password = PasswordField('确认新密码', validators=[DataRequired(message='请确认密码')])


# 重置密码校验
class ResetPasswordValidator(BaseValidator):
    new_password = PasswordField('新密码', validators=[
        DataRequired(message='新密码不可为空'),
        Regexp(r'^[A-Za-z0-9_*&$#@]{6,22}$', message='密码长度必须在6~22位之间，包含字符、数字和 _ '),
        EqualTo('confirm_password', message='两次输入的密码不一致，请输入相同的密码')
    ])
    confirm_password = PasswordField('确认新密码', validators=[DataRequired(message='请确认密码')])


# 更改密码校验
class ChangePasswordValidator(ResetPasswordValidator):
    old_password = PasswordField('原密码', validators=[DataRequired(message='不可为空')])


class UserEmailValidator(ClientValidator):
    account = StringField(validators=[Email(message='无效email')])
    secret = StringField(validators=[
        DataRequired(),
        # password can only include letters, numbers and "_"
        Regexp(r'^[A-Za-z0-9_*&$#@]{6,22}$')
    ])
    nickname = StringField(validators=[
        DataRequired(),
        length(min=2, max=22)
    ])


class UpdateUserValidator(BaseValidator):
    username = StringField(validators=[length(min=2, max=10, message='用户名长度必须在2~10之间'), Optional()])

    email = StringField(validators=[Email(message='无效email'), Optional()])
    mobile = StringField(validators=[
        length(min=11, max=11, message='手机号为11个数字'),
        Regexp(r'^1(3|4|5|7|8)[0-9]\d{8}$'),
        Optional()
    ])
    nickname = StringField()

class CreateUserValidator(UpdateUserValidator, CreatePasswordValidator):
    username = StringField(validators=[
        DataRequired(message='用户名不可为空'),
        length(min=2, max=10, message='用户名长度必须在2~10之间')])


class UpdateAvatarValidator(BaseValidator):
    avatar = StringField('头像', validators=[
        DataRequired(message='请输入头像url')
    ])
