import tornado_mysql
import pymysql
from tornado_mysql import pools

from config import DATABASE

pymysql.install_as_MySQLdb()


class Connect(object):
    """异步连接数据库类"""
    def __init__(self):
        self.config = DATABASE.get('default', {})
        self.connection = pymysql.connections.Connection(**self.config)
        self.cursor = self.connection.cursor()
        self.dict_cursor = self.connection.cursor(cursor=pymysql.cursors.DictCursor)

    def close(self):
        self.connection.close()
        self.dict_cursor.close()
        self.cursor.close()


def connect():
    """连接默认数据库"""
    config = DATABASE.get('default', {})
    conn = pymysql.connections.Connection(**config)
    return conn.cursor(cursor=pymysql.cursors.DictCursor)


def async_connect():
    """异步连接"""
    config = DATABASE.get('default', {})
    config.update({
        'autocommit': True,
        'cursorclass': tornado_mysql.cursors.DictCursor,
    })
    return tornado_mysql.connect(**config)


def async_pool():
    """连接池"""
    config = DATABASE.get('default', {})
    config.update({
        'cursorclass': tornado_mysql.cursors.DictCursor,
    })
    pool = pools.Pool(config, max_idle_connections=1, max_recycle_sec=3)
    return pool
