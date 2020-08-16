import json
import os
import time
import uuid

from tornado import gen

from config import DEFAULT_UPLOAD_PATH, DOMAIN
from db.sql_utils.question import get_paged_questions, get_question_by_str, get_filtered_questions, check_user_has_read, \
    get_question_by_qid, create_question, delete_question_by_id
from db.sql_utils.tag import get_all_tags
from handlers.base_handlers import BaseHandler
from utils.auth import login_required
from utils.err_code import PARAMETER_ERR, CREATE_ERR, DEL_ERR


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


class QuestionDetailHandler(BaseHandler):
    @gen.coroutine
    def get(self, qid, *args, **kwargs):
        user = self.current_user
        try:
            qid = int(qid)
        except Exception as e:
            self.json_response(*PARAMETER_ERR)
            raise gen.Return()
        if user:
            yield check_user_has_read(user, qid)
        data = yield get_question_by_qid(qid)
        self.render('question_detail.html', data={
            'question': data
        })


class QuestionCreateHandler(BaseHandler):
    @gen.coroutine
    @login_required
    def get(self, *args, **kwargs):
        tags = yield get_all_tags()
        self.render('question_create.html', data={
            'tags': tags,
        })

    @gen.coroutine
    @login_required
    def post(self, *args, **kwargs):
        tag_id = self.get_argument('tag_id', '')
        abstract = self.get_argument('abstract', '')
        content = self.get_argument('content', '')
        user = self.current_user
        try:
            tag_id = int(tag_id)
        except Exception as e:
            self.json_response(*PARAMETER_ERR)
            raise gen.Return()
        data, qid = yield create_question(tag_id, user, abstract, content)
        if not data:
            self.json_response(*CREATE_ERR)
            raise gen.Return()
        self.json_response(200, 'ok', data={
            'qid': qid,
        })


class QuestionUploadPicHandler(BaseHandler):
    @gen.coroutine
    @login_required
    def get(self, *args, **kwargs):
        self.json_response(200, 'ok', data={})

    @gen.coroutine
    @login_required
    def post(self, *args, **kwargs):
        pics = self.request.files.get('pic', None)
        urls = []
        if not pics:
            self.json_response(*PARAMETER_ERR)
            raise gen.Return()
        folder_name = time.strftime('%Y%m%d', time.localtime())
        folder = os.path.join(DEFAULT_UPLOAD_PATH, folder_name)
        if not os.path.exists(folder):
            os.makedirs(folder)
        for pic in pics:
            filename = str(uuid.uuid4()) + pic['filename']
            with open(os.path.join(folder, filename), 'wb+') as f:
                f.write(pic['body'])
            web_pic_path = 'pics/' + folder_name + '/' + filename
            urls.append(os.path.join(DOMAIN, web_pic_path))
        self.write(json.dumps({
            'success': True,
            'msg': 'ok',
            'file_path': urls,
        }))


class QuestionDeleteHandler(BaseHandler):
    @gen.coroutine
    def get(self, *args, **kwargs):
        pass

    @gen.coroutine
    @login_required
    def post(self, qid, *args, **kwargs):
        user = self.current_user
        try:
            qid = int(qid)
        except Exception as e:
            self.json_response(*PARAMETER_ERR)
            raise gen.Return()
        result = yield delete_question_by_id(qid, user)
        if not result:
            self.json_response(*DEL_ERR)
            raise gen.Return()
        self.json_response(200, 'ok', data={})
