#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: Huang Wei
import aiofiles

async def async_read_file(filepath):
    try:
        async with aiofiles.open(filepath, 'r') as f:
            return await f.read()
    except FileNotFoundError as e:
        print(e)
        return None

async def async_write_file(filepath, content):
    """
    往文件中写内容(不附加)
    :param filepath:
    :param content:
    :return:
    """
    if not isinstance(content, str):
        content = str(content)
    async with aiofiles.open(filepath, mode='w', encoding='utf-8') as f:
        await f.write(content)

if __name__ == '__main__':
    import asyncio

    async def test():
        await async_write_file('test.txt', '123')
        content = await async_read_file('test.txt')
        print(content)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(test())