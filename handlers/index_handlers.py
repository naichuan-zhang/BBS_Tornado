from tornado import gen

from db.sql_utils.tag import get_all_tags
from handlers.base_handlers import BaseHandler


class IndexHandler(BaseHandler):
    @gen.coroutine
    def get(self, *args, **kwargs):
        tags = yield get_all_tags()
        self.render('index.html', data={'tags': tags})
