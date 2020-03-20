#coding: utf-8
import threading
import MySQLdb
from DBUtils.PersistentDB import PersistentDB
from utils.common import deprecated

from contextlib import contextmanager

class Isolation:
    """
    事务隔离级别
    sql example: set session transaction isolation level read committed
    """
    READ_UNCOMMITTED = "read uncommitted"
    READ_COMMITTED = "read committed"
    REPEATABLE= "repeatable read"
    SERIALIZABLE = "serializable"


class MysqlConn:
    """
    mysql客户端连接类
    用法：
    1.子类继承MysqlConn，继承的类就代表了某个数据库的连接。
    class MysqlConnYunying(MysqlConn):
        _conf = {}
    2. with MysqlConnYunying.create() as (conn, c):
            ...
    """
    _pool = None
    _lock = threading.Lock()
    _conf = None

    @classmethod
    def create(cls, conf=None, **kargs):
        """
        创建mysql连接池
        :param conf:  连接mysql服务器的配置
        :param kargs:  连接mysql服务器的补充配置
        :return:
        """
        conf = conf or cls._conf
        conf.update(kargs)
        if 'charset' not in conf:
            conf.update('charset', 'utf8')

        if not cls._pool:
            with cls._lock:
                if not cls._pool:
                    print('create pool')
                    #创建的连接池不一定是属于MysqlConn父类的，也可能是子类，如果cls是子类的话,那cls._pool相当于
                    #为子类添加一个类属性_pool
                    cls._pool = PersistentDB(creator=MySQLdb, maxusage=0, **conf)

        return cls()

    def __enter__(self):
        self.conn = self._pool.connection()
        self.cursor = self.conn.cursor()
        return (self.conn, self.cursor)

    def __exit__(self, type, value, trace):
        self.cursor.close()
        self.conn.close()


class MysqlConnYunying(MysqlConn):
    """
    创建运营数据库连接
    """
    _conf = {'host': '', 'user': '', 'passwd': '', 'db': '', 'port':3306, 'charset': 'utf8'}


class MysqlConnCrmReader(MysqlConn):
    """
    创建crm只读连接
    """
    _conf = {'host': '', 'user': '', 'passwd': '', 'db': '', 'port':3306, 'charset': 'utf8'}

@deprecated
@contextmanager
def mysqldb_conn(conf):
    """
    使用连接池创建mysql连接
    用法是:
    with  mysqldb_conn(conf) as conn:
        with cursor(conn) as c:
            ....
    这种方式也可以用，不过更推荐用class MysqlConn的方式来连接mysql.
    :param conf:
    :return:
    """
    try:
        _db = PersistentDB(
            creator=MySQLdb,
            maxusage=0,
            host=conf['host'],
            user=conf['user'],
            passwd=conf['passwd'],
            db=conf['db'],
            charset='utf8')
        conn = _db.connection()
        yield conn
    except Exception as e:
        print(e)
        conn.rollback()
    finally:
        conn.close()

@deprecated
@contextmanager
def cursor(conn, **kargs):
    """
    创建一个会话
    :param conn:
    :param kargs:
    :return:
    """
    c = conn.cursor()
    keys = kargs.keys()
    if 'isolation' in keys:
        c.execute("set session transaction isolation level %s" % kargs['isolation'])
    try:
        yield c
    finally:
        c.close()



if __name__ == '__main__':
    cursor_conf = {}
    cursor_conf['isolation'] = Isolation.READ_UNCOMMITTED
    with MysqlConnCrmReader.create() as (conn, c):
        c.execute('select * from cuser where phone=%s', ['13750062604'])
        data = c.fetchone()
        print(data)

    with MysqlConnYunying.create() as (conn, c):
        c.execute('select count(1) from baidu_toufang')
        data = c.fetchone()
        print(data)

    with MysqlConnCrmReader.create() as (conn, c):
        c.execute('select * from cuser where phone=%s', ['13750062604'])
        data = c.fetchone()

    with MysqlConnYunying.create() as (conn, c):
        c.execute('select count(1) from baidu_toufang')
        data = c.fetchone()
        print(data)

    print(MysqlConnCrmReader._pool)
    print(MysqlConnYunying._pool)