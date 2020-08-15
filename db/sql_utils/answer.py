from tornado import gen
from tornado_mysql import escape_string

from db.sql_utils.connect import async_connect


@gen.coroutine
def get_answers(qid):
    conn = yield async_connect()
    cursor = conn.cursor()
    sql = "select * from t_answer a left join t_user u on u.uid = a.uid where qid=%d order by a.created_at asc" % qid
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
def check_answers(qid):
    conn = yield async_connect()
    cursor = conn.cursor()
    sql = "update t_answer set has_read = 1 where qid=%d" % qid
    try:
        data = yield cursor.execute(sql)
    except Exception as e:
        data = 0
    finally:
        cursor.close()
        conn.close()
    raise gen.Return(data)


@gen.coroutine
def create_answer(qid, user, content):
    conn = yield async_connect()
    cursor = conn.cursor()
    if isinstance(content, str):
        content = escape_string(content)
    sql1 = "insert into t_answer(qid, uid, content) " \
           "values (%d, (select uid from t_user where username='%s'), '%s')" % (int(qid), user, content)
    sql2 = "update t_question set answer_count = answer_count + 1 where qid = %d" % qid
    try:
        data = yield cursor.execute(sql1)
        yield cursor.execute(sql2)
    except Exception as e:
        data = 0
    finally:
        cursor.close()
        conn.close()
    raise gen.Return(data)


@gen.coroutine
def get_answer_status(user):
    conn = yield async_connect()
    cursor = conn.cursor()
    sql = """
        select sum(c) as answer_count from
        (select qid, count(qid) as c from t_answer where has_read=1 group by qid) as a where a.qid in
        (select qid from t_question where uid=(select uid from t_user where username='%s'))
    """ % user
    try:
        yield cursor.execute(sql)
        data = cursor.fetchone()
    except Exception as e:
        data = {}
    finally:
        cursor.close()
        conn.close()
    raise gen.Return(data)


@gen.coroutine
def adopt_answer(aid, qid):
    conn = yield async_connect()
    cursor = conn.cursor()
    sql = "update t_answer set status=true where aid=%d and qid=(select qid from t_question qid=%d)" % (aid, qid)
    try:
        data = yield cursor.execute(sql)
    except Exception as e:
        data = 0
    finally:
        cursor.close()
        conn.close()
    raise gen.Return(data)

