from tornado import gen

from db.sql_utils.connect import async_connect


@gen.coroutine
def get_paged_questions(page_count=10, last_qid=None, pre=False):
    conn = yield async_connect()
    cursor = conn.cursor()
    if not pre:  # 前页
        if not last_qid:
            sql = "select q.qid, q.abstract, q.content, q.view_count, q.answer_count, u.username, t.tag_name " \
                  "from t_question q left join t_user u on q.uid = u.uid left join t_tag t on q.tid = t.tid " \
                  "order by qid desc limit %d" % page_count
        else:
            sql = "select q.qid, q.abstract, q.content, q.view_count, q.answer_count, u.username, t.tag_name " \
                  "from t_question q left join t_user u on q.uid = u.uid left join t_tag t on q.tid = t.tid " \
                  "where qid < %d order by qid desc limit %d" % (last_qid, page_count)
    else:  # 后页
        if not last_qid:
            return []
        else:
            sql = "select q.qid, q.abstract, q.content, q.view_count, q.answer_count, u.username, t.tag_name " \
                  "from t_question q left join t_user u on q.uid = u.uid left join t_tag t on q.tid = t.tid " \
                  "where qid >= %d order by qid desc limit %d" % (last_qid, page_count)
    try:
        yield cursor.execute(sql)
        data = cursor.fetchall()
    except Exception as e:
        data = []
    finally:
        cursor.close()
        conn.close()
    raise gen.Return(data)


@gen.coroutine
def get_question_by_str(s):
    conn = yield async_connect()
    cursor = conn.cursor()
    sql = "select q.qid, q.abstract, q.view_count, q.answer_count, q.created_at, q.updated_at, u.username, t.tag_name " \
          "from t_question q left join t_user u on q.uid = u.uid left join t_tag t on t.tid = q.tid " \
          "where abstract like binary '%{}%' or content like binary '%{}%'".format(s, s)
    try:
        yield cursor.execute()
        data = cursor.fetchall()
    except Exception as e:
        data = []
    finally:
        cursor.close()
        conn.close()
    raise gen.Return(data)


@gen.coroutine
def get_filtered_questions(name, user=None, tag=None):
    conn = yield async_connect()
    cursor = conn.cursor()
    if name == 'newest':
        sql = "SELECT q.qid, q.abstract, q.content, q.view_count, q.answer_count, u.username, t.tag_name " \
              "FROM t_question q LEFT JOIN t_user u ON q.uid=u.uid LEFT JOIN t_tag t ON q.tid=t.tid " \
              "ORDER BY q.created_at DESC LIMIT 15"
    elif name == 'hotest':
        sql = "SELECT q.qid, q.abstract, q.content, q.view_count, q.answer_count, u.username, t.tag_name " \
              "FROM t_question q LEFT JOIN t_user u ON q.uid=u.uid LEFT JOIN t_tag t ON q.tid=t.tid " \
              "ORDER BY q.answer_count DESC LIMIT 15"
    elif name == 'under':
        sql = "SELECT q.qid, q.abstract, q.content, q.view_count, q.answer_count, u.username, t.tag_name " \
              "FROM t_question q LEFT JOIN t_user u ON q.uid=u.uid LEFT JOIN t_tag t ON q.tid=t.tid " \
              "where q.status=0 order by q.created_at desc limit 15"
    elif name == 'hasdone':
        sql = "SELECT q.qid, q.abstract, q.content, q.view_count, q.answer_count, u.username, t.tag_name " \
              "FROM t_question q LEFT JOIN t_user u ON q.uid=u.uid LEFT JOIN t_tag t ON q.tid=t.tid " \
              "where q.status=1 order by q.created_at desc limit 15"
    elif name == 'prefer' and user:
        sql = """
            select * from t_question q left join t_user u on q.uid = u.uid left join t_tag t on q.tid = t.tid where q.tid = (
            select tid from t_question where uid = (select uid from t_user where u.username='%s')
            group by tid order by count(tid) desc limit 1)
            """
    elif tag:
        sql = "SELECT q.qid, q.abstract, q.content, q.view_count, q.answer_count, u.username, t.tag_name " \
              "FROM t_question q LEFT JOIN t_user u ON q.uid=u.uid LEFT JOIN t_tag t ON q.tid=t.tid" \
              " where q.tid=%d order by answer_count desc limit 15" % tag
    else:
        raise gen.Return([])
    try:
        yield cursor.execute(sql)
        data = cursor.fetchall()
    except Exception as e:
        data = []
    finally:
        cursor.close()
        conn.close()
    raise gen.Return(data)