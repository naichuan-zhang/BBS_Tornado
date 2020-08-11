import base64
import hashlib
import uuid
from io import BytesIO
from urllib import parse

from tornado import gen

from db.sql_utils.auth import get_user_by_username, create_user
from handlers.base_handlers import BaseHandler
from utils.auth_code import get_pic_code
from utils.err_code import LOGIN_VCODE_ERR, USERNAME_ERR, PASSWORD_ERR, USER_EXISTS, USER_CREATE_ERR


class LoginHandler(BaseHandler):
    @gen.coroutine
    def get(self, *args, **kwargs):
        self.render('login.html')

    @gen.coroutine
    def post(self, *args, **kwargs):
        sign = self.get_argument('sign', '')
        vcode = self.get_argument('vcode', '')
        username = self.get_argument('username', '')
        password = self.get_argument('password', '')
        if self.get_secure_cookie(sign).decode('utf-8') != vcode:
            # 如果验证码错误
            self.json_response(*LOGIN_VCODE_ERR)
            raise gen.Return()
        data = yield get_user_by_username(username)
        if not data:
            self.json_response(*USERNAME_ERR)
            raise gen.Return()
        if data.get('password') != hashlib.sha1(password.encode('utf-8')).hexdigest():
            self.json_response(*PASSWORD_ERR)
            raise gen.Return()
        self.set_secure_cookie('auth-user', data.get('username', ''))
        self.set_cookie('username', data.get('username', ''), expires_days=30)
        self.json_response(200, 'ok', {})


class LogoutHandler(BaseHandler):
    @gen.coroutine
    def get(self, *args, **kwargs):
        next = self.get_argument('next', '')
        self.clear_cookie('auth-user')
        self.clear_cookie('username')
        next = next + '?' + parse.urlencode({'m': '注销成功', 'e': 'success'})
        self.redirect(next)


class SignupHandler(BaseHandler):
    @gen.coroutine
    def get(self, *args, **kwargs):
        # 渲染页面
        self.render('login.html')

    @gen.coroutine
    def post(self, *args, **kwargs):
        # 提交注册数据
        username = self.get_argument('username', '')
        password = self.get_argument('password', '')
        vcode = self.get_argument('vcode', '')
        sign = self.get_argument('sign', '')
        # 检验验证码是否正确
        if self.get_secure_cookie(sign).decode('utf-8') != vcode:
            self.json_response(*LOGIN_VCODE_ERR)
            raise gen.Return()
        data = yield get_user_by_username(username)
        if data:
            self.json_response(*USER_EXISTS)
            raise gen.Return()
        password = hashlib.sha1(password.encode('utf-8')).hexdigest()
        result = yield create_user(username, password)
        if not result:
            self.json_response(*USER_CREATE_ERR)
            raise gen.Return()
        self.set_secure_cookie('auth-user', username)
        self.set_cookie('username', username, expires_days=30)
        self.json_response(200, 'ok', {})


class AuthCodeHandler(BaseHandler):
    @gen.coroutine
    def get(self, *args, **kwargs):
        b = BytesIO()
        img, check = yield get_pic_code()
        img.save(b, format='png')
        vcode = base64.b64encode(b.getvalue())
        sign = str(uuid.uuid1())
        self.set_secure_cookie(sign, ''.join([str(i) for i in check]).lower(), expires_days=1/48)
        self.json_response(200, 'ok', {
            'vcode': str(vcode.decode('utf-8')),
            'sign': str(sign),
        })
