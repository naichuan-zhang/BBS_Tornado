from tornado import gen

from db.sql_utils.connect import async_connect


@gen.coroutine
def get_all_tags():
    conn = yield async_connect()
    cursor = conn.cursor()
    sql = "select tid, tag_name from t_tag order by tid"
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
def get_tag_list():
    conn = yield async_connect()
    cursor = conn.cursor()
    sql = """select d.tid, d.tag_name, sum(d.qcount) question_count, sum(d.ucount) user_count from (
            select tid, tag_name, count(tid) qcount, uid, username, count(uid) ucount from (
            select q.qid, t.tag_name, t.tid, u.username, u.uid from t_question q left join t_tag t on t.tid = q.tid left join t_user u on q.uid = u.uid
            ) c group by tid, uid) d order by question_count desc"""
    try:
        yield cursor.execute(sql)
        data = cursor.fetchall()
    except Exception as e:
        data = []
    finally:
        cursor.close()
        conn.close()
    raise gen.Return(data)

