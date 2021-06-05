from flask import request, json
from app.core.utils import jsonify
from werkzeug.exceptions import HTTPException

class APIException(HTTPException):
    code = 500  # http 状态码
    msg = '服务器未知错误'  # 异常信息
    error_code = 999  # 约定的异常码

    def __init__(self, code=None, error_code=None, msg=None, headers=None):
        if code:
            self.code = code
        if error_code:
            self.error_code = error_code
        if msg:
            self.msg = msg
        super(APIException, self).__init__()

    def get_body(self, environ=None):
        body = dict(
            msg=self.msg,
            error_code=self.error_code,
            request_url=request.method + ' ' + self.get_url_no_param()
        )
        text = json.dumps(body)  # 返回文本
        return text

    def get_headers(self, environ=None):
        return [('Content-type', 'application/json; charset=utf-8')]

    @staticmethod
    def get_url_no_param():
        full_path = str(request.full_path)
        main_path = full_path.split('?')[0]
        return main_path


class Success(APIException):
    '''
    0/200: 查询成功
    1/201: 创建 | 更新成功
    2/203: 删除成功
    '''
    code = 200
    error_code = 0
    data = None
    msg = '成功'

    def __init__(self, data=None, code=None, error_code=None, msg=None):
        if data:
            self.data = jsonify(data)
        if error_code == 1:
            code = code if code else 201
            msg = msg if msg else '创建 | 更新成功'
        if error_code == 2:
            code = code if code else 202
            msg = msg if msg else '删除成功'
        super(Success, self).__init__(code, error_code, msg)

    def get_body(self, environ=None):
        body = dict(
            error_code=self.error_code,
            msg=self.msg,
            data=self.data
        )
        text = json.dumps(body)  # 返回文本
        return text


class ServerError(APIException):
    code = 500
    error_code = 999
    msg = '服务器端异常'


class Failed(APIException):
    code = 400
    error_code = 9999
    msg = '失败'

##########  权限相关(10000~10100)  ##########
class AuthFailed(APIException):
    code = 401
    error_code = 10000
    msg = '授权失败'


class Forbidden(APIException):
    code = 403
    error_code = 10010
    msg = '权限不足，禁止访问'

##########  查询相关(10100~10200)  ##########
class NotFound(APIException):
    code = 404  # http 状态码
    error_code = 10100  # 约定的异常码
    msg = '未查询到数据'  # 异常信息


class RepeatException(APIException):
    code = 400
    error_code = 10110
    msg = '重复数据'


class ParameterException(APIException):
    code = 400
    error_code = 10120
    msg = '参数错误'


########## Token相关(10200~10300) ##########
class TokenException(APIException):
    code = 401
    error_code = 10200
    msg = 'Token已过期或无效Token'


############################################
##########  登录相关(11000~12000)  ##########
############################################
class ClientTypeError(APIException):
    code = 400
    error_code = 11000
    msg = '登录方式无效'


class AtLeastOneClientException(APIException):
    code = 400
    error_code = 11010
    msg = '无法解绑，至少保留一种登录方式'


############################################
########## 用户类错误(20000~30000) ##########
############################################
class UserException(APIException):
    code = 404
    error_code = 20000
    msg = '用户类通用错误'


class UserNotFound(APIException):
    code = 404
    error_code = 20010
    msg = '没有找到相关用户'


class IdentityException(APIException):
    code = 404
    error_code = 21000
    msg = '用户身份错误'


############################################
########## 商品类错误(30000~40000) ##########
############################################
class ProductException(APIException):
    code = 404
    error_code = 30000
    msg = '产品类通用错误'


class ProductNotFound(APIException):
    code = 404
    error_code = 30010
    msg = '没有找到相关产品'


class CategoryException(APIException):
    code = 404
    error_code = 31000
    msg = '类别类通用错误'


class CategoryNotFound(APIException):
    code = 404
    error_code = 31010
    msg = '没有找到相关类别'


############################################
########## 活动类错误(40000~50000) ##########
############################################

class BannerException(APIException):
    code = 404
    error_code = 40000
    msg = 'Banner类通用错误'


class BannerNotFound(APIException):
    code = 404
    error_code = 40010
    msg = '没有找到相关Banner'


class ThemeException(APIException):
    code = 404
    error_code = 41000
    msg = '主题类通用错误'


class ThemeNotFound(APIException):
    code = 404
    error_code = 41010
    msg = '没有找到相关主题'


############################################
########## 订单类错误(50000~60000) ##########
############################################
class OrderException(APIException):
    code = 404
    error_code = 50000
    msg = '订单类通用错误'


class OrderNotFound(APIException):
    code = 404
    error_code = 50010
    msg = '没有找到相关订单'


