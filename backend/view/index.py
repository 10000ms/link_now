# -*- coding: utf-8 -*-
"""
    index
    ~~~~~~~~~

    主页HTTP处理类模块

    内含：主页（静态文件，开启xsrf_token），登陆以及注册页面

    :copyright: (c) 2018 by Victor Lai.

"""
import random
from hashlib import sha256
import re
import json
import uuid

import tornado
from tornado.web import RequestHandler

import config
from utils import (
    get_redis_fetch_data,
    get_mongo_fetch_data,
)


class StaticFileHandler(tornado.web.StaticFileHandler):

    def __init__(self, *args, **kwargs):
        super(StaticFileHandler, self).__init__(*args, **kwargs)
        self.xsrf_token


class LoginHandler(RequestHandler):

    def __init__(self, *args, **kwargs):
        super(LoginHandler, self).__init__(*args, **kwargs)
        self.db_checker = self.application.mongodb['user']
        self.redis = self.application.redis

    def get(self, *args, **kwargs):
        messages = []
        url = RequestHandler.reverse_url(self, 'login')
        return self.render('index/login.html', url=url, messages=messages)

    async def post(self, *args, **kwargs):
        """
        处理用户登陆

        :param args:
        :param kwargs:
        :return: 失败返回失败信息并返回登陆页面，成功跳转聊天室
        """
        messages = []
        url = RequestHandler.reverse_url(self, 'login')
        account = self.get_body_argument('account')
        # 检测帐号是否合法
        if not Support.check_account(account):
            messages.append('帐号不合法')
            return self.render('index/login.html', url=url, messages=messages)
        password = self.get_body_argument('password')

        json_user_data = {
            'account': account,
        }
        mongo_res = await get_mongo_fetch_data(json_user_data, '/user/login')
        get_data = json.loads(mongo_res)
        status = get_data['status']

        # 检测是否存在该用户
        if status != 'ok':
            messages.append('未找到用户')
            return self.render('index/login.html', url=url, messages=messages)
        # 检测密码是否正确
        if not Support.check_password(password, get_data['password']):
            messages.append('密码错误')
            return self.render('index/login.html', url=url, messages=messages)

        # 检测单点登陆
        redis_res = await get_redis_fetch_data(json_user_data, '/session/check_login')
        get_redis_data = json.loads(redis_res)
        if get_redis_data['status'] != 'ok':
            messages.append('用户已登陆')
            return self.render('index/login.html', url=url, messages=messages)
        print(get_data)
        self.set_secure_cookie('chat_room_username', get_data['username'])

        # 通过所有检测

        # 获取聊天室url地址
        chat_room_url = RequestHandler.reverse_url(self, 'chat')
        # 获取单点登陆的token
        user_token_value = Support.single_login_token()
        # 设置单点登陆的cookie
        self.set_secure_cookie('user_token', user_token_value)
        # 设置用户账户的cookie
        self.set_secure_cookie('account', account)
        # 设置用户名的cookie
        # self.set_secure_cookie("chat_room_username", get_user["username"])
        # Redis记录单点登陆token
        session_data = {
            'account': account,
            'session': user_token_value,
        }
        await get_redis_fetch_data(session_data, '/session/add')
        # 跳转聊天室
        return self.redirect(chat_room_url)


class RegisterHandler(RequestHandler):

    def __init__(self, *args, **kwargs):
        super(RegisterHandler, self).__init__(*args, **kwargs)
        self.db_checker = self.application.mongodb['user']
        self.redis = self.application.redis

    def get(self, *args, **kwargs):
        messages = []
        url = RequestHandler.reverse_url(self, 'register')
        return self.render('index/register.html', url=url, messages=messages)

    async def post(self, *args, **kwargs):
        """
        处理用户注册
        :param args:
        :param kwargs:
        :return: 失败返回失败信息并返回注册页面，成功跳转聊天室
        """
        messages = []
        url = RequestHandler.reverse_url(self, 'register')
        account = self.get_body_argument('account', default=None, strip=True)
        # 检查账户是否存在并是否合法
        if Support.check_account(account) is False:
            messages.append('账户已存在或帐号不合法')
            return self.render('index/register.html', url=url, messages=messages)
        password = self.get_body_argument('password', default=None, strip=True)
        confirm = self.get_body_argument('confirm', default=None, strip=True)
        # 检查两次输入密码是否相同
        if not password or not confirm:
            messages.append('请输入密码和重复密码')
            return self.render('index/register.html', url=url, messages=messages)
        if password != confirm:
            messages.append('两次输入的密码不一致')
            return self.render('index/register.html', url=url, messages=messages)
        email = self.get_body_argument('email', default=None, strip=True)
        # email检查
        if len(email) < 4:
            messages.append('请输入正确格式的邮箱')
            return self.render('index/register.html', url=url, messages=messages)
        username = self.get_body_argument('username', default=None, strip=True)
        # 用户名检查
        if len(username) <= 2:
            messages.append('用户名过短')
            return self.render('index/register.html', url=url, messages=messages)

        # 生产sha256密码
        sha256_password = Support.get_password(password)

        json_user_data = {
            'account': account,
            'password': sha256_password,
            'username': username,
            'email': email,
        }
        res = await get_mongo_fetch_data(json_user_data, '/user/register')
        status = json.loads(res)
        status = status['status']
        if status == 'ok':
            # 获取聊天室url地址
            chat_room_url = RequestHandler.reverse_url(self, 'chat')
            # 获取单点登陆的token
            user_token_value = Support.single_login_token()
            # 设置单点登陆的cookie
            self.set_secure_cookie('user_token', user_token_value)
            # 设置用户账户的cookie
            self.set_secure_cookie('account', account)
            # 设置用户名的cookie
            self.set_secure_cookie('chat_room_username', username)
            # Redis记录单点登陆token
            session_data = {
                'account': account,
                'session': user_token_value,
            }
            await get_redis_fetch_data(session_data, '/session/add')
            # 跳转聊天室
            return self.redirect(chat_room_url)
        else:
            messages.append('邮箱或用户名已存在')
            return self.render('index/register.html', url=url, messages=messages)


class Support(object):
    """
    辅助处理类
    """

    @staticmethod
    def get_password(pw):
        """
        原始密码生成sha256加盐码
        :param pw: 密码
        :return: sha256加盐码
        """
        # 加入随机数字
        num = random.randint(100, 10000)
        sha256_maker = sha256()
        pw = str(pw) + str(config.settings['cookie_secret']) + str(num)
        pw = pw.encode('utf-8')
        sha256_maker.update(pw)
        # 前面加入该随机数字，用于解密
        return str(num) + '|' + sha256_maker.hexdigest()

    @staticmethod
    def check_password(need_check_pw, old_pw):
        """
        检测用户密码是否正确
        :param need_check_pw: 用户输入的密码
        :param old_pw: 数据库中用户密码
        :return: 正确为True，错误为False
        """
        num = old_pw.split('|', 1)[0]
        older = old_pw.split('|', 1)[1]
        sha256_maker = sha256()
        need_check_pw = str(need_check_pw) + str(config.settings['cookie_secret']) + str(num)
        need_check_pw = need_check_pw.encode('utf-8')
        sha256_maker.update(need_check_pw)
        if sha256_maker.hexdigest() == older:
            return True
        else:
            return False

    @staticmethod
    def check_account(account):
        """
        检测帐号是否合法
        :param account: 用户输入帐号
        :return: 合法为True，不合法为False
        """
        check_re = re.compile(r'\w{6,20}')
        re_match = re.match(check_re, account)
        if re_match:
            return True
        else:
            return False

    @staticmethod
    def single_login_token():
        """
        生成单点登陆用token
        :return: token
        """
        return str(uuid.uuid4())
