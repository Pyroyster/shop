from flask import current_app, g

from app.core.redprint import Redprint
from app.core.token_auth import auth
from app.libs.error_code import Success
from app.models.user import User
from app.dao.user import UserDao
from app.dao.identity import IdentityDao
from app.validators.forms import ChangePasswordValidator, \
    CreateUserValidator, UpdateUserValidator, UpdateAvatarValidator
from app.core.utils import get_request_args

api = Redprint(name='user', module='用户')


@api.route('', methods=['GET'])
@auth.login_required
def get_user():
    user = User.get(id=g.user.id)
    return Success(data=user)


@api.route('', methods=['POST'])
def create_user():
    form = CreateUserValidator().nt_data
    UserDao.create_user(form)
    return Success(error_code=1)

@api.route('',method=['PUT'])
@auth.login_required()
def update_user():
    form = UpdateUserValidator().nt_data
    UserDao.update_info(uid=g.user.id, form=form)
    return Success(error_code=1)


@api.route('/bind', methods=['PUT'])
@auth.login_required
def bind_identity():
    validator = get_request_args()
    IdentityDao.bind(user_id=g.user.id, identifier=validator.account, type=validator.type)
    return Success(error_code=1)


@api.route('/bind', methods=['PUT'])
@auth.login_required
def unbind_identity():
    '''解绑账号'''
    validator = get_request_args()
    IdentityDao.unbind(user_id=g.user.id, type=validator.type)
    return Success(error_code=1)


@api.route('', methods=['DELETE'])
@auth.login_required
def delete_user():
    UserDao.delete_user(uid=g.user.id)
    return Success(error_code=2)


@api.route('/password', methods=['PUT'])
@auth.login_required
def change_password():
    validator = ChangePasswordValidator().nt_data
    UserDao.change_password(
        uid = g.user.id,
        old_pwd = validator.old_pwd,
        new_pwd = validator.new_pwd
    )
    return Success(error_code=1)


@api.route('/avatar', methods=['PUT'])
@auth.login_required
def set_avatar():
    validator = UpdateAvatarValidator().nt_data
    UserDao.set_avatar(id=g.user.id, avatar=validator.avatar)
    return Success(error_code=1, msg='头像更改成功')


