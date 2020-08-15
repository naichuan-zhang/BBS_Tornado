import tornadoredis

from config import REDIS

config = REDIS.get('default', {})
connection_pool = tornadoredis.ConnectionPool(max_connections=500, wait_for_available=True)


def redis_connect():
    return tornadoredis.Client(**config, connection_pool=connection_pool)
