import os
import sys

from tornado import web, httpserver, ioloop

from config import SETTINGS, DATABASE
from router import ROUTERS
from utils.logger import logger

log = logger('admin')


class Application(web.Application):
    def __init__(self):
        super(Application, self).__init__(ROUTERS, **SETTINGS)


if __name__ == '__main__':
    args = sys.argv[1:]
    if args[0] == 'run':
        # 启动项目
        app = Application()
        print("Starting server on port 9000...")
        server = httpserver.HTTPServer(app)
        server.listen(9000)
        server.start()
        ioloop.IOLoop.instance().start()
    elif args[0] == 'dbshell':
        # 连接到数据库cli
        config = DATABASE.get('default', {})
        os.system('mysql -u{user} -p{password} -D{database} -A'.format(
            user=config.get('user', 'root'),
            password=config.get('password', ''),
            database=config.get('database', 'bbs')
        ))
    elif args[0] == 'migrate':
        # 数据迁移
        config = DATABASE.get('default', {})
        init_sql = 'mysql -u{user} -p{password} -D{database} -A < database/migration.sql'.format(
            user=config.get('user', 'root'),
            password=config.get('password', ''),
            database=config.get('database', 'bbs')
        )
        print("Initializing tables to database {}...".format(config.get('database')))
        data = os.system(init_sql)
        if data == 256:
            log.info('Seems like you havent\'t create the database, try:\n \'create database tequila default '
                     'character set utf8;\'')
            print('Seems like you havent\'t create the database, try:\n \'create database tequila default character '
                  'set utf8;\'')
        print('Completed.')
    elif args[0] == 'shell':
        # 打开ipython解析器
        os.system('ipython')
    elif args[0] == 'help':
        print("""following arguments available:
                <migrate> for migrating tables to your database,
                <shell> for using ipython shell,
                <dbshell> connect current database,
                <run> run a tornado web server.""")
    else:
        print('Arguments Error. using \'help\' get help.')