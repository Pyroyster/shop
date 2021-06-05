from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature

from flask import current_app

from app.libs.enums import ClientTypeEnum
from app.core.token_auth import generate_auth_token
from app.models.identity import Identity
from app.models.user import User
from app.libs.error_code import AuthFailed, IdentityException


class LoginVerifyService:
    @staticmethod
    def get_token(account, secret, type):
        promise = {
            ClientTypeEnum.USERNAME: LoginVerifyService.verify_by_username,  # 账号&密码登录
            ClientTypeEnum.EMAIL: LoginVerifyService.verify_by_email,  # 邮箱&密码登录
            ClientTypeEnum.MOBILE: LoginVerifyService.verify_by_mobile,  # 手机号&密码登录
            ClientTypeEnum.WX_MINA: LoginVerifyService.verify_by_wx_mina,  # 微信·小程序登录
            ClientTypeEnum.WX_OPEN: LoginVerifyService.verify_by_wx_open,  # 微信·开发平台登录(web端扫码登录)
            ClientTypeEnum.WX_ACCOUNT: LoginVerifyService.verify_by_wx_account  # 微信第三方登录(公众号H5端)
        }
        identity = promise[ClientTypeEnum(type)](account, secret)  # 如verify_by_username(account, secret)
        expiration = current_app.config['TOKEN_EXPIRATION']  # token有效期
        token = generate_auth_token(identity['uid'],
                                    type.value,
                                    identity['scope'],
                                    expiration)
        return token

    @staticmethod
    def validate_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token, return_header=True)  # return一个列表，列表中有两个字典
        except BadSignature:
            raise AuthFailed(msg='token失效，请重新登录', error_code=1002)
        except SignatureExpired:
            raise AuthFailed(msg='token过期，请重新登录', error_code=1003)

        rv = {
            'scope': data[0]['scope'],  # 用户权限
            'uid': data[0]['uid'],  # 用户ID
            'create_at': data[1]['iat'],  # 创建时间
            'expire_in': data[1]['exp']  # 有效期
        }

        return rv

    @staticmethod
    def verify_by_username(username, password):
        identity = Identity.get_or_404(identity=username, type=ClientTypeEnum.USERNAME.value,
                                       e=IdentityException(msg='用户尚未注册'))  # type为Integer类型
        identity.check_password(password, e=AuthFailed(msg='密码错误'))  # 调用check_password_hash()
        user = User.get(id=identity.user_id)
        return {'uid': user.id, 'scope': user.auth_scope}

    @staticmethod
    def verify_by_email(email, password):
        identity = Identity.get_or_404(identity=email, type=ClientTypeEnum.EMAIL.value,
                                       e=IdentityException(msg='该邮箱未注册'))  # type为Integer类型
        identity.check_password(password, e=AuthFailed(msg='密码错误'))  # 调用check_password_hash()
        user = User.get(id=identity.user_id)
        return {'uid': user.id, 'scope': user.auth_scope}

    @staticmethod
    def verify_by_phone(phone, password):
        identity = Identity.get_or_404(identity=phone, type=ClientTypeEnum.MOBILE.value,
                                       e=IdentityException(msg='该手机号未注册'))  # type为Integer类型
        identity.check_password(password, e=AuthFailed(msg='密码错误'))  # 调用check_password_hash()
        user = User.get(id=identity.user_id)
        return {'uid': user.id, 'scope': user.auth_scope}

    @staticmethod
    def verify_by_username(username, password):
        identity = Identity.get_or_404(identity=username, type=ClientTypeEnum.USERNAME.value,
                                       e=IdentityException(msg='用户尚未注册'))  # type为Integer类型
        identity.check_password(password, e=AuthFailed(msg='密码错误'))  # 调用check_password_hash()
        user = User.get(id=identity.user_id)
        return {'uid': user.id, 'scope': user.auth_scope}

    @staticmethod
    def verify_by_username(username, password):
        identity = Identity.get_or_404(identity=username, type=ClientTypeEnum.USERNAME.value,
                                       e=IdentityException(msg='用户尚未注册'))  # type为Integer类型
        identity.check_password(password, e=AuthFailed(msg='密码错误'))  # 调用check_password_hash()
        user = User.get(id=identity.user_id)
        return {'uid': user.id, 'scope': user.auth_scope}

    @staticmethod
    def verify_by_username(username, password):
        identity = Identity.get_or_404(identity=username, type=ClientTypeEnum.USERNAME.value,
                                       e=IdentityException(msg='用户尚未注册'))  # type为Integer类型
        identity.check_password(password, e=AuthFailed(msg='密码错误'))  # 调用check_password_hash()
        user = User.get(id=identity.user_id)
        return {'uid': user.id, 'scope': user.auth_scope}
