from functools import wraps
from collections import namedtuple

from flask import current_app, g, request
from flask_httpauth import HTTPBasicAuth as _HTTPBasicAuth
from itsdangerous import TimedJSONWebSignatureSerializer \
    as Serializer, BadSignature, SignatureExpired

from app.models.user import User
from app.libs.error_code import AuthFailed
from app.core.auth import is_in_auth_scope


class HTTPBasicAuth(_HTTPBasicAuth):
    def __init__(self, scheme=None, realm=None):
        super(HTTPBasicAuth, self).__init__(scheme, realm)
        self.hash_password = None  # self.hash_password_callback = None
        self.verify_password = None  # self.verify_password_callback = None

    def admin_required(self, f):
        @wraps(f)
        def decorator(*args, **kwargs):
            auth = request.authorization
            if request.method != 'OPTIONS':
                [username, client_password] = [auth.username, auth.password] \
                    if auth else ['', '']
                if self.verify_admin_callback:
                    self.verify_admin_callback(username, client_password)
            return f(*args, **kwargs)
        return decorator()

    def verify_admin(self, f):
        self.verify_admin_callback = f
        return f

    def group_required(self, f):
        @wraps(f)
        def decorator(*args, **kwargs):
            auth = request.authorization
            if request.method != 'OPTIONS':
                [username, client_password] = [auth.username, auth.password] \
                    if auth else ['', '']
                if self.verify_group_callback:
                    self.verify_group_callback(username, client_password)
            return f(*args, **kwargs)

        return decorator()

    def verify_group(self, f):
        self.verify_group_callback = f
        return f


auth = HTTPBasicAuth()
UserTuple = namedtuple('User', ['uid', 'ac_type', 'scope'])

# super admin
@auth.verify_admin
def verify_admin(token, password):
    (uid, ac_type, score) = validate_token(token)
    current_user = User.get_or_404(id=uid)
    if not current_user.is_admin:
        raise AuthFailed(msg='该接口为超级管理员权限操作')
    g.user = current_user

@auth.verify_group
def verify_group(token, password):
    (uid, ac_type, scope) = validate_token(token)
    current_user = User.get_or_404(id=uid)
    group_id = current_user.group_id
    if not current_user.is_admin:
        if group_id is None:
            raise AuthFailed(msg='您还不属于任何权限组，请联系系统管理员获得权限')
        allowed = is_in_auth_scope(group_id, request.endpoint)
        if not allowed:
            raise AuthFailed(msg='权限不够，请联系系统管理员获得权限')


@auth.verify_password  # 对应login_require
def verify_password(token, paaaword):
    user_data = verify_auth_token(token)
    if not user_data:
        return False
    g.user = User.get_or_404(id=user_data.uid)
    return True


def verify_auth_token(token):
    (uid, ac_type, scope) = validate_token(token)
    return UserTuple(uid, ac_type, scope)


def validate_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        user_data = s.loads(token)
    except BadSignature:
        raise AuthFailed(msg='token 无效', error_code=1002)
    except SignatureExpired:
        raise AuthFailed(msg='token 过期', error_code=1003)
    uid = user_data['uid']
    ac_type = user_data['type']  # 登录方式
    scope = user_data['scope']
    return UserTuple(uid, ac_type, scope)


def generate_auth_token(uid, ac_type, scope=None, expiration=7200):
    s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
    token = s.dumps({
        'uid': uid,
        'type': ac_type,
        'scope': scope
    }).decode('ascii')
    return {'token': token}

"""
config = config['production']

r = redis.Redis(connection_pool=pool)

key_access_token = config.KEY_ACCESS_TOKEN
key_refresh_token = config.KEY_REFRESH_TOKEN
access_token_expires = config.ACCESS_TOKEN_EXPIRES
refresh_token_expires = config.REFRESH_TOKEN_EXPIRES


def get_token():
    token = request.headers.get('Authorization', None)
    if token is None:
        return None, None

    try:
        access_token = token.split(';')[0]
        refresh_token = token.split(';')[1]
    except IndexError:
        access_token = token.split(';')[0]
        refresh_token = None

    return access_token, refresh_token


def generate_token(user, token_type, expires):
    # dumps all of user data or dumps user's id
    s = Serializer(current_app.secret_key, expires_in=expires)
    token = s.dumps({'id': user.id}).decode('ascii')
    time_expires = time() + expires
    key = 'token: ' + token_type
    # ,有序set操作
    r.zadd(key, {token: expires})

    return token





def generate_token_info(user):

    access_token = generate_token(user, 'access', access_token_expires)
    refresh_token = generate_token(user, 'refresh', refresh_token_expires)
    token_info = {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'expires_access': access_token_expires,
        'expires_refresh': refresh_token_expires
    }

    return token_info
"""
