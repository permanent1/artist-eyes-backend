from datetime import timedelta

from app.exceptions.exception import AuthenticationError
from app.models.user import User
from app.services.auth import jwt_helper, hashing, random_code_verifier
from app.services.auth.oauth2_schema import OAuth2CellphoneRequest, OAuth2PasswordRequest, OAuth2WXCellphoneRequest
from app.support.helper import alphanumeric_random
from config.auth import settings
from app.services.auth.wx_decrypt import WXBizDataCrypt  # 微信解密库

import logging


def create_token_response_from_user(user):
    expires_delta = timedelta(minutes=settings.JWT_TTL)
    expires_in = int(expires_delta.total_seconds())
    token = jwt_helper.create_access_token(user.id, expires_delta)

    return {
        "token_type": "bearer",
        "expires_in": expires_in,
        "access_token": token,
    }


class PasswordGrant:
    def __init__(self, request_data: OAuth2PasswordRequest):
        self.request_data = request_data

    def respond(self):
        user = User.get_or_none(User.username == self.request_data.username)
        if not user:
            raise AuthenticationError(message='Incorrect email or password')

        # 用户密码校验
        if not (user.password and hashing.verify_password(self.request_data.password, user.password)):
            raise AuthenticationError(message='Incorrect email or password')

        # 用户状态校验
        if not user.is_enabled():
            raise AuthenticationError(message='Inactive user')

        return create_token_response_from_user(user)


class CellphoneGrant:
    def __init__(self, request_data: OAuth2CellphoneRequest):
        self.request_data = request_data

    def respond(self):
        cellphone = self.request_data.cellphone
        code = self.request_data.verification_code
        if not random_code_verifier.check(cellphone, code):
            raise AuthenticationError(message='Incorrect verification code')

        user = User.get_or_none(User.cellphone == cellphone)
        # 验证通过，用户不存在则创建
        if not user:
            username = 'srcp_' + alphanumeric_random()
            password = hashing.get_password_hash(alphanumeric_random())
            user = User.create(cellphone=cellphone, username=username, password=password)

        # 用户状态校验
        if not user.is_enabled():
            raise AuthenticationError(message='Inactive user')

        return create_token_response_from_user(user)


class WXCellphoneGrant:
    def __init__(self, request_data: OAuth2WXCellphoneRequest):
        self.request_data = request_data

    def respond(self):
        appid = settings.WX_APP_ID  # 小程序的App ID
        encrypted_data = self.request_data.encryptedData
        iv = self.request_data.iv
        session_key = self.request_data.session_key

        # 解密微信加密数据
        wx_crypt = WXBizDataCrypt(appid, session_key)
        try:
            decrypted_data = wx_crypt.decrypt(encrypted_data, iv)
        except Exception as e:
            raise AuthenticationError(message='Failed to decrypt data')

        # 获取手机号
        cellphone = decrypted_data.get('phoneNumber')
        logging.info('login user cellphone: %s ' % (cellphone))
        if not cellphone:
            raise AuthenticationError(message='Failed to retrieve phone number')

        # 根据手机号查找用户
        user = User.get_or_none(User.cellphone == cellphone)

        # 如果用户不存在，创建新用户
        if not user:
            username = 'wx_' + alphanumeric_random()
            password = hashing.get_password_hash(alphanumeric_random())
            user = User.create(cellphone=cellphone, username=username, password=password)

        # 用户状态校验
        if not user.is_enabled():
            raise AuthenticationError(message='Inactive user')

        return create_token_response_from_user(user)