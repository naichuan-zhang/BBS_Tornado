from tornado import gen

from db.sql_utils.connect import async_connect


@gen.coroutine
def get_user_by_username(username):
    conn = yield async_connect()
    cursor = conn.cursor()
    sql = "select username, email, password from t_user where username='%s'" % username
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
def create_user(username, password):
    conn = yield async_connect()
    cursor = conn.cursor()
    sql = "insert into t_user(username, password) values ('%s', '%s')" % (username, password)
    try:
        data = yield cursor.execute(sql)
    except Exception as e:
        data = 0
    finally:
        cursor.close()
        conn.close()
    raise gen.Return(data)


@gen.coroutine
def get_group_by_user(username):
    conn = yield async_connect()
    cursor = conn.cursor()
    sql = "select group_type from t_user where username='%s'" % username
    try:
        yield cursor.execute(sql)
        data = cursor.fetchone()
    except Exception as e:
        data = None
    finally:
        cursor.close()
        conn.close()
    raise gen.Return(data)
