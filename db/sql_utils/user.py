from tornado import gen

from db.sql_utils.connect import async_connect


@gen.coroutine
def get_user_list():
    conn = yield async_connect()
    cursor = conn.cursor()
    sql = "select (@r:=@r+1) as ranks, username, point from t_user u, (select (@r:=0)) c " \
          "where u.group_type = 0 order by u.point desc limit 50"
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
def get_user_by_str(s):
    conn = yield async_connect()
    cursor = conn.cursor()
    sql = "select ranks, username, point from (select (@r:=@r+1) as ranks, username, point " \
          "from t_user u, (select (@r:=0)) c where u.group_type = 0 order by u.point desc) d" \
          " where username like binary '%{}%'".format(s)
    try:
        yield cursor.execute(sql)
        data = cursor.fetchall()
    except Exception as e:
        data = []
    finally:
        cursor.close()
        conn.close()
    raise gen.Return(data)
