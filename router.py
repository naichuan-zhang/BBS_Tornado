from handlers.index_handlers import IndexHandler

ROUTERS = [
    (r'/', IndexHandler),       # 首页
    (r'/index', IndexHandler),
]

