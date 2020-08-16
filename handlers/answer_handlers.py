import json

from tornado import gen, web

from db.nosql_utils.channels import ANSWER_STATUS_CHANNEL
from db.nosql_utils.connect import redis_connect
from db.sql_utils.answer import get_answers, check_answers, create_answer, get_answer_status, delete_answer_by_id, \
    update_question_answer
from handlers.base_handlers import BaseHandler
from utils.auth import login_required
from utils.err_code import PARAMETER_ERR, USER_HAS_NOT_VALIDATE, CREATE_ERR, DEL_ERR
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


class AnswerDeleteHandler(BaseHandler):
    @gen.coroutine
    @login_required
    def get(self, *args, **kwargs):
        pass

    @gen.coroutine
    @login_required
    def post(self, aid, *args, **kwargs):
        qid = self.get_argument('qid', '')
        try:
            qid = int(qid)
        except Exception as e:
            self.json_response(*PARAMETER_ERR)
            raise gen.Return()
        try:
            aid = int(aid)
        except Exception as e:
            self.json_response(*PARAMETER_ERR)
            raise gen.Return()
        user = self.current_user
        result = yield delete_answer_by_id(aid, qid, user)
        up_result = yield update_question_answer(qid)
        if (not result) or (not up_result):
            self.json_response(*DEL_ERR)
            raise gen.Return()
        self.json_response(200, 'ok', data={})


class AnswerStatusHandler(BaseHandler):
    def initialize(self):
        self.redis = redis_connect()
        self.redis.connect()

    @web.asynchronous
    def get(self, *args, **kwargs):
        if self.request.connection.stream.closed():
            raise gen.Return()
        self.register()

    @gen.engine
    def register(self):
        yield gen.Task(self.redis.subscribe, ANSWER_STATUS_CHANNEL)
        self.redis.listen(self.on_response)

    def on_response(self, data):
        if data.kind == 'message':
            try:
                self.write(data.body)
                self.finish()
            except Exception as e:
                print(e)
        elif data.kind == 'unsubscribe':
            self.redis.disconnect()

    def on_connection_close(self):
        self.finish()
