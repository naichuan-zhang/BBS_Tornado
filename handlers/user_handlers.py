from tornado import gen

from db.sql_utils.user import get_user_list, get_user_by_str
from handlers.base_handlers import BaseHandler
from utils.auth import login_required
from utils.err_code import PARAMETER_ERR


class UserListHandler(BaseHandler):
    @gen.coroutine
    @login_required
    def get(self, *args, **kwargs):
        data = yield get_user_list()
        my_data = {}
        if data:
            for user in data:
                if user.get('username') == self.current_user:
                    my_data = {
                        'username': user.get('username'),
                        'point': user.get('point'),
                        'rank': user.get('ranks'),
                    }
        self.render('user_list.html', data={
            'user_list': data,
            'current_user': my_data,
        })


class UserSearchHandler(BaseHandler):
    @gen.coroutine
    @login_required
    def get(self, *args, **kwargs):
        s = self.get_argument('s', '')
        if not 2 <= len(s) <= 12:
            self.json_response(*PARAMETER_ERR)
            raise gen.Return()
        data = yield get_user_by_str(s)
        self.json_response(200, 'ok', data={
            'user_list': data,
        })
