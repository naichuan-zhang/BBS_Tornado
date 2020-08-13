from handlers.auth_handlers import SignupHandler, LoginHandler, LogoutHandler, AuthCodeHandler
from handlers.index_handlers import IndexHandler

# index
from handlers.question_handlers import QuestionListHandler, QuestionSearchHandler, QuestionFilterHandler

ROUTERS = [
    (r'/', IndexHandler),  # 首页
    (r'/index', IndexHandler),
]

# auth
ROUTERS += [
    (r'/auth/signup', SignupHandler),  # 注册
    (r'/auth/login', LoginHandler),  # 登录
    (r'/auth/logout', LogoutHandler),  # 注销
    (r'/auth/v.img', AuthCodeHandler),  # 验证码
]

# question
ROUTERS += [
    (r'/question/list', QuestionListHandler),  # 问题列表
    (r'/question/search', QuestionSearchHandler),  # 问题搜索
    (r'/question/filter/(\w+)', QuestionFilterHandler),  # 问题过滤
]
