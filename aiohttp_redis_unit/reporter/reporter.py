# -*- coding: utf-8 -*-
import asyncio
import json
import time
import collections

import aiohttp

from utils import (
    set_logging,
    MessageType,
)
from config import config
from redis_part import RedisConn


class ReporterComponent:
    logger = set_logging(config.REPORTER_LOGGER_NAME)
    message_db = RedisConn(
        host=config.REDIS_HOST,
        port=config.REDIS_PORT,
        db=config.MESSAGE_DB
    ).db
    remote_db = RedisConn(
        host=config.REDIS_HOST,
        port=config.REDIS_PORT,
        db=config.REMOTE_DB
    ).db
    group_db = RedisConn(
        host=config.REDIS_HOST,
        port=config.REDIS_PORT,
        db=config.GROUP_DB
    ).db


def get_url(remote, url):
    return str(remote) + str(url)


async def fetch(session, url, data):
    ReporterComponent.logger.info('发生post：' + str(url) + str(data))
    async with session.post(url, data=data) as response:
        return await response.text()


async def deal_single_user_message(user_message, session):
    message = json.loads(user_message)
    remote = ReporterComponent.remote_db.get(message['id'])
    if message.get('method') is None:
        message['method'] = 'user_message'
        message['g_id'] = message['id']
        user_message = json.dumps(message)
    if remote is not None:
        remote = remote
        url = get_url(remote, '/api/user_message')
        await fetch(session, url, user_message)


async def check_group_data(group_id, session):
    send_data = {
        'group_id': group_id
    }
    send_data = json.dumps(send_data)
    url = 'http://' + config.MONGODB_URL['host'] + ':' + config.MONGODB_URL['port'] + '/user/get_group'
    group_user = await fetch(session, url, send_data)
    group_user = json.loads(group_user)
    print('group_user ', group_user)
    if isinstance(group_user, dict) and group_user.get('status') and group_user['status'] == 'ok':
        for user in group_user['account']:
            ReporterComponent.group_db.sadd(group_id, user)
    else:
        raise ValueError


async def deal_group_message(group_message, session):
    message = json.loads(group_message)
    group_id = message['id']
    await check_group_data(group_id, session)
    users = ReporterComponent.group_db.smembers(group_id)
    user_message = message
    user_message['method'] = 'user_message'
    remote_user_dict = collections.defaultdict(list)
    for user in users:
        user_remote = ReporterComponent.remote_db.get(user)
        if user_remote is not None:
            remote_user_dict[user_remote].append(user)
    for remote, t_id in remote_user_dict.items():
        url = get_url(remote, '/api/users_message')
        user_message['g_id'] = t_id
        send_user_message = json.dumps(user_message)
        await fetch(session, url, send_user_message)


async def deal_all_message(all_message, session):
    users = ReporterComponent.remote_db.keys()
    users_message = json.loads(all_message)
    users_message['g_id'] = users
    users_message['method'] = 'user_message'
    users_message = json.dumps(users_message)
    remotes = ReporterComponent.remote_db.smembers(config.REMOTE_NAME)
    for remote in remotes:
        url = get_url(remote, '/api/users_message')
        await fetch(session, url, users_message)


async def deal_system_message(system_message, session):
    user_message = json.loads(system_message)
    new_message = user_message['message']
    new_message['g_id'] = user_message['id']
    new_message['id'] = user_message['id']
    new_message = json.dumps(new_message)
    await deal_single_user_message(new_message, session)


async def one_step(session):
    user_message = ReporterComponent.message_db.rpop(str(MessageType.user_message.value))
    group_message = ReporterComponent.message_db.rpop(str(MessageType.group_message.value))
    all_message = ReporterComponent.message_db.rpop(str(MessageType.all_message.value))
    system_message = ReporterComponent.message_db.rpop(str(MessageType.system_message.value))
    if user_message is None and group_message is None and all_message is None and system_message is None:
        time.sleep(0.1)
    else:
        if user_message is not None:
            await deal_single_user_message(user_message, session)
        if group_message is not None:
            await deal_group_message(group_message, session)
        if all_message is not None:
            await deal_all_message(all_message, session)
        if system_message is not None:
            await deal_system_message(system_message, session)


async def main_reporter():
    async with aiohttp.ClientSession() as session:
        ReporterComponent.logger.info('启动main_reporter')
        while True:
            await one_step(session)


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main_reporter())
