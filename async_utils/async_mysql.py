#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Huang Wei
import asyncio
import aiomysql

class Isolation:
    READ_UNCOMMITTED = "read uncommitted"
    READ_COMMITTED = "read committed"
    REPEATABLE= "repeatable read"
    SERIALIZABLE = "serializable"


class MysqlConnAsync:
    """
    目前这个锁还不是分布式锁，如果对于多进程下是没办法做到只有一个连接池的。
    不过由于进程间是相互隔离的，数据是不共享的，我们很难把一个连接池给其它进程用，所以多进程下每个进程创建
    一个连接池也是合理的。
    """
    _pool = None
    _lock = asyncio.Lock()
    _conf = None

    @classmethod
    async def pool(cls, loop, conf=None, **kargs):
        conf = conf or cls._conf
        conf.update(kargs)

        if not cls._pool:
            async with cls._lock:
                if not cls._pool:
                    print('create pool')
                    cls._pool = await aiomysql.create_pool(loop=loop, charset='utf8', **conf)

        return cls._pool


class MysqlConnYunyingAsync(MysqlConnAsync):
    _conf = {}


class MysqlConnCrmReaderAsync(MysqlConnAsync):
    _conf = {}


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    # from utils.common import write_file

    async def mysql_test1():
        pool = await MysqlConnCrmReaderAsync().pool(loop)
        async with pool.acquire() as conn:
            async with conn.cursor() as c:
                await c.execute('select * from cuser where phone=%s', ['13750062604'])
                data = await c.fetchone()
                print(data)

        # print('111')
        # write_file('test.txt', data)
        # print('222')


    async def mysql_test2():
        pool = await MysqlConnYunyingAsync().pool(loop)
        async with pool.acquire() as conn:
            async with conn.cursor() as c:
                await c.execute('select count(1) from baidu_toufang')
                data = await c.fetchone()
                print(data)

        # print('333')
        # write_file('test.txt', data)
        # print('444')


    async def main():
        await mysql_test1()
        await mysql_test2()
        await mysql_test1()
        await mysql_test1()
        print(MysqlConnYunyingAsync._pool)
        print(MysqlConnCrmReaderAsync._pool)
        print(MysqlConnAsync._pool)

    loop.run_until_complete(main())
    # print(MysqlConnYunyingAsync.lock)


