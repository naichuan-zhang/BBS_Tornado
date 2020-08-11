from handlers.auth_handlers import SignupHandler, LoginHandler, LogoutHandler, AuthCodeHandler
from handlers.index_handlers import IndexHandler

# index
ROUTERS = [
    (r'/', IndexHandler),       # 首页
    (r'/index', IndexHandler),
]

# auth
ROUTERS += [
    (r'/auth/signup', SignupHandler),   # 注册
    (r'/auth/login', LoginHandler),     # 登录
    (r'/auth/logout', LogoutHandler),   # 注销
    (r'/auth/v.img', AuthCodeHandler),  # 验证码
]


