import json

from tornado import gen

from db.nosql_utils.channels import ANSWER_STATUS_CHANNEL
from db.nosql_utils.connect import redis_connect
from db.sql_utils.answer import get_answers, check_answers, create_answer, get_answer_status
from handlers.base_handlers import BaseHandler
from utils.auth import login_required
from utils.err_code import PARAMETER_ERR, USER_HAS_NOT_VALIDATE, CREATE_ERR
from utils.json_encoder import JsonEncoder


class AnswerListHandler(BaseHandler):
    @gen.coroutine
    def get(self, qid, *args, **kwargs):
        try:
            qid = int(qid)
        except Exception as e:
            self.json_response(*PARAMETER_ERR)
            raise gen.Return()
        data = yield get_answers(qid)
        yield check_answers(qid)    # 更新未读答案
        self.json_response(200, 'ok', data={
            'answer_list': data,
        })


class AnswerCreateHandler(BaseHandler):
    def initialize(self):
        self.redis = redis_connect()
        self.redis.connect()

    @gen.coroutine
    @login_required
    def post(self, *args, **kwargs):
        qid = self.get_argument('qid', '')
        content = self.get_argument('content', '')
        user = self.current_user
        try:
            qid = int(qid)
        except Exception as e:
            self.json_response(*PARAMETER_ERR)
            raise gen.Return()
        if not user:
            self.json_response(*USER_HAS_NOT_VALIDATE)
            raise gen.Return()
        data = yield create_answer(qid, user, content)
        answer_status = yield get_answer_status(user)
        if not data:
            self.json_response(*CREATE_ERR)
            raise gen.Return()
        yield gen.Task(self.redis.publish, ANSWER_STATUS_CHANNEL,
                       json.dumps(answer_status, cls=JsonEncoder))
        self.json_response(200, 'ok', data={})
