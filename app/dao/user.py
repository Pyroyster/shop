from app.core.db import db
from app.models.user import User
from app.models.identity import Identity
from app.libs.enums import ScopeEnum,ClientTypeEnum
from app.dao.identity import IdentityDao


class UserDao:
    @staticmethod
    def create_user(form):
        with db.auto_commit():
            user = User.create(
                commit=False,
                nickname=getattr(form, 'nickname', None),
                auth=ScopeEnum.COMMON.value
            )
            if(hasattr(form, 'username')):
                Identity.abort_repeat(identifier=form.username, msg='该用户名已被注册，请重新输入用户名')
                Identity.create(commit=False, user_id=user.id, type=ClientTypeEnum.USERNAME.value, verified=1,
                                identifier=form.username, password=form.password)
            if (hasattr(form, 'mobile')):
                Identity.abort_repeat(identifier=form.mobile, msg='手机号已被使用，请重新输入新的手机号')
                Identity.create(commit=False, user_id=user.id, type=ClientTypeEnum.MOBILE.value,
                                identifier=form.mobile, password=form.password)
            if (hasattr(form, 'email')):
                Identity.abort_repeat(identifier=form.email, msg='邮箱已被使用，请重新输入新的邮箱号')
                Identity.create(commit=False, user_id=user.id, type=ClientTypeEnum.EMAIL.value,
                                identifier=form.email, password=form.password)


    @staticmethod
    def register_by_wx_mina():
        pass

    @staticmethod
    def register_by_wx_open():
        pass

    @staticmethod
    def register_by_wx_account():
        pass

    @staticmethod
    def change_password(uid, old_pwd, new_pwd):
        identity = Identity.get_or_404(user_id=uid)
        if identity.validate_password(old_pwd):
            identity_list = Identity.query.filter(
                Identity.type.in_([
                    ClientTypeEnum.USERNAME.value,
                    ClientTypeEnum.EMAIL.value,
                    ClientTypeEnum.MOBILE.value]),
                Identity.user_id == uid
            ).all()
            with db.auto_commit():
                for item in identity_list:
                    item.update(commit=False, password=new_pwd)

    @staticmethod
    def reset_password():
        pass

    @staticmethod
    def update_info(uid, form):
        identity_infos = []
        if (hasattr(form, 'username')):
            identity_infos.append(
                {'identifier': form.username, 'type': ClientTypeEnum.USERNAME.value, 'msg': '该用户名已被使用，请重新输入新的用户名'})
        if (hasattr(form, 'mobile')):
            identity_infos.append(
                {'identifier': form.mobile, 'type': ClientTypeEnum.MOBILE.value, 'msg': '手机号已被使用，请重新输入新的手机号'})
        if (hasattr(form, 'email')):
            identity_infos.append(
                {'identifier': form.email, 'type': ClientTypeEnum.EMAIL.value, 'msg': '邮箱已被使用，请重新输入新的邮箱号'})
        # 第2步: 修改用户信息
        with db.auto_commit():
            # 第2.1步: 获取用户信息
            user = User.query.filter_by(id=uid).first_or_404()
            credential = IdentityDao.get_credential(user_id=uid)
            # 第2.2步: 修改用户昵称
            if hasattr(form, 'nickname'):
                user.update(commit=False, nickname=form.nickname)
            # 第2.3步: 依次修改用户身份信息(用户名、手机号、邮箱)
            for item in identity_infos:
                Identity.abort_repeat(identifier=item['identifier'], msg=item['msg'])
                IdentityDao.update_identity(
                    commit=False, user_id=uid, identifier=item['identifier'], credential=credential, type=item['type']
                )

    @staticmethod
    def set_avatar(id, avatar):
        with db.auto_commit():
            user = User.get(id=id)
            user._avatar = avatar

    @staticmethod
    def delete_user(uid):
        user = User.query.filter_by(id=uid).first_or_404()
        with db.auto_commit():
            Identity.query.filter_by(user_id=user.id).delete(commit=False)
            user.delete(commit=False)


