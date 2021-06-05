from flask import current_app

from app.core.redprint import Redprint
from app.libs.error_code import Success
from app.validators.forms import ClientValidator, TokenValidator
from app.service.login_verify import LoginVerifyService

api = Redprint(name='token', module='令牌')


@api.route('', methods=['POST'])
def get_token():
    form = ClientValidator().nt_data
    token = LoginVerifyService.get_token(
        account=form.account, secret=form.secret, type=form.type
    )
    return Success(data=token)


@api.route('/open_redirect_url', method=['GET'])
def get_open_redirect_url():
    return Success(data={'redirect_url': current_app.config['OPEN_AUTHORIZE_URL']})