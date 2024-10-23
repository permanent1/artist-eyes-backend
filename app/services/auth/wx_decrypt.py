import base64
import json
from Crypto.Cipher import AES
from app.exceptions.exception import AuthenticationError

class WXBizDataCrypt:
    def __init__(self, appid, session_key):
        self.appid = appid
        self.session_key = session_key

    def decrypt(self, encrypted_data, iv):
        """
        解密微信加密数据
        :param encrypted_data: 微信接口返回的加密数据
        :param iv: 微信接口返回的初始向量
        :return: 解密后的数据
        """
        # 对 session_key 和 iv 进行 base64 解码
        session_key = base64.b64decode(self.session_key)
        iv = base64.b64decode(iv)
        encrypted_data = base64.b64decode(encrypted_data)

        try:
            cipher = AES.new(session_key, AES.MODE_CBC, iv)
            decrypted_data = self._unpad(cipher.decrypt(encrypted_data))
            decrypted_data = json.loads(decrypted_data)

            if decrypted_data['watermark']['appid'] != self.appid:
                raise AuthenticationError(message='Invalid Buffer')

            return decrypted_data
        except Exception as e:
            raise AuthenticationError(message='Decryption failed')

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]

