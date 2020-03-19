#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
使用redis做了一个分布式锁，用法:
with dist_lock(key):
    ...
"""
import time
from contextlib import contextmanager

import redis

REDIS_LOCK_CONFIG = {
    'ip': '127.0.0.1',
    'port': 6379,
    'db': 11
}

DEFAULT_EXPIRES = 600
DEFAULT_RETRIES = 5

client = redis.Redis(connection_pool=redis.BlockingConnectionPool(
    max_connections=15, host=REDIS_LOCK_CONFIG['ip'], port=REDIS_LOCK_CONFIG['port']), db=REDIS_LOCK_CONFIG['db'])

@contextmanager
def dist_lock(key):
    key = 'lock_%s' % key
    try:
        t = _acquire_lock(key, client)
        yield t
    finally:
        _release_lock(key, client)


def ask_lock(key):
    key = 'lock_%s' % key
    if client.get(key):
        return True
    else:
        return False

def _acquire_lock(key, client):
    while 1:
        get_stored = client.get(key)
        if get_stored:
            time.sleep(0.03)
        else:
            if client.setnx(key, 1):
                client.expire(key, DEFAULT_EXPIRES)
                return True


def _release_lock(key, client):
    client.delete(key)
