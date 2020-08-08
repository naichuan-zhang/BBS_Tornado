from tornado import gen

from handlers.base_handlers import BaseHandler
from utils.err_code import LOGIN_VCODE_ERR


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
        # TODO: to be continued ...
