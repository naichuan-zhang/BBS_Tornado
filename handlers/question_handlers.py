from tornado import gen

from db.sql_utils.question import get_paged_questions, get_question_by_str, get_filtered_questions
from handlers.base_handlers import BaseHandler
from utils.err_code import PARAMETER_ERR


class QuestionListHandler(BaseHandler):
    @gen.coroutine
    def get(self, *args, **kwargs):
        last_qid = self.get_argument('lqid', None)
        pre = self.get_argument('pre', '0')
        if last_qid:
            try:
                last_qid = int(last_qid)
            except Exception as e:
                self.json_response(200, 'ok', {
                    'question_list': [],
                    'last_qid': None,
                })
        pre = True if pre == '1' else False
        data = yield get_paged_questions(page_count=15, last_qid=last_qid, pre=pre)
        lqid = data[-1].get('qid') if data else None
        self.json_response(200, 'ok', {
            'question_list': data,
            'last_qid': lqid,
        })


class QuestionSearchHandler(BaseHandler):
    @gen.coroutine
    def get(self, *args, **kwargs):
        s = self.get_argument('s', '')
        if not 3 < len(s) < 14:
            self.render('search_result.html', data={'result': [], 'msg': '参数不符合要求！'})
            raise gen.Return()
        data = yield get_question_by_str(s)
        self.render('search_result.html', data={'result': data, 'msg': ''})


class QuestionFilterHandler(BaseHandler):
    @gen.coroutine
    def get(self, name='', *args, **kwargs):
        if name in ['newest', 'hotest', 'under', 'hasdone', 'prefer']:
            data = yield get_filtered_questions(name, user=self.current_user)
        elif name.startswith('t_'):
            try:
                tid = int(name.split('_')[1])
            except Exception as e:
                self.json_response(*PARAMETER_ERR)
                raise gen.Return()
            data = yield get_filtered_questions(name, user=self.current_user, tag=tid)
        else:
            self.json_response(*PARAMETER_ERR)
            raise gen.Return()
        self.json_response(200, 'ok', data={
            'question_list': data,
        })
