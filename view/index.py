# -*- coding: utf-8 -*-
import random
from hashlib import md5
import re

import tornado
from tornado.web import RequestHandler

import config


class StaticFileHandler(tornado.web.StaticFileHandler):

    def __init__(self, *args, **kwargs):
        super(StaticFileHandler, self).__init__(*args, **kwargs)
        self.xsrf_token


class LoginHandler(RequestHandler):

    def get(self, *args, **kwargs):
        messages = []
        url = RequestHandler.reverse_url(self, "login")
        return self.render("index/login.html", url=url, messages=messages)

    def post(self, *args, **kwargs):
        messages = []
        url = RequestHandler.reverse_url(self, "login")
        account = self.get_body_argument("account")
        if not Support.check_account(account):
            messages.append("帐号不合法")
            return self.render("index/login.html", url=url, messages=messages)
        password = self.get_body_argument("password")
        db_checker = self.application.mongodb["user"]
        get_user = db_checker.find_one({"account": account})
        if not get_user:
            messages.append("未找到用户")
            return self.render("index/login.html", url=url, messages=messages)
        if not Support.check_password(password, get_user["password"]):
            messages.append("密码错误")
            return self.render("index/login.html", url=url, messages=messages)
        if self.application.redis.hexists("user_token", account):
            messages.append("用户已登陆")
            return self.render("index/login.html", url=url, messages=messages)
        else:
            chat_room_url = RequestHandler.reverse_url(self, "chat")
            user_token_value = Support.single_login_token(account)
            self.set_secure_cookie("user_token", user_token_value)
            self.set_secure_cookie("chat_room_user", account)
            self.set_secure_cookie("chat_room_username", get_user["username"])
            self.application.redis.hset("user_token", account, user_token_value)
            return self.redirect(chat_room_url)


class RegisterHandler(RequestHandler):

    def get(self, *args, **kwargs):
        messages = []
        url = RequestHandler.reverse_url(self, "register")
        return self.render("index/register.html", url=url, messages=messages)

    def post(self, *args, **kwargs):
        messages = []
        url = RequestHandler.reverse_url(self, "register")
        db_checker = self.application.mongodb["user"]
        account = self.get_body_argument("account", default=None, strip=True)
        get_user = db_checker.find_one({"account": account})
        if get_user or not Support.check_account(account):
            messages.append("帐号不合法")
            return self.render("index/register.html", url=url, messages=messages)
        password = self.get_body_argument("password", default=None, strip=True)
        confirm = self.get_body_argument("confirm", default=None, strip=True)
        if not password or not confirm:
            messages.append("请输入密码和重复密码")
            return self.render("index/register.html", url=url, messages=messages)
        if password != confirm:
            messages.append("两次输入的密码不一致")
            return self.render("index/register.html", url=url, messages=messages)
        email = self.get_body_argument("email", default=None, strip=True)
        if len(email) < 4:
            messages.append("请输入正确格式的邮箱")
            return self.render("index/register.html", url=url, messages=messages)
        get_email = db_checker.find_one({"email": email})
        if get_email:
            messages.append("注册邮箱已存在")
            return self.render("index/register.html", url=url, messages=messages)
        username = self.get_body_argument("username", default=None, strip=True)
        if len(username) <= 2:
            messages.append("用户名过短")
            return self.render("index/register.html", url=url, messages=messages)
        md5_password = Support.get_password(password)
        user_data = [{
            'account': account,
            'password': md5_password,
            'username': username,
            'email': email,
        }, ]
        db_checker.insert(user_data)
        chat_room_url = RequestHandler.reverse_url(self, "chat")
        user_token_value = Support.single_login_token(account)
        self.set_secure_cookie("user_token", user_token_value)
        self.set_secure_cookie("chat_room_user", account)
        self.set_secure_cookie("chat_room_username", username)
        self.application.redis.hset("user_token", account, user_token_value)
        return self.redirect(chat_room_url)


class Support(object):

    @staticmethod
    def get_password(pw):
        num = random.randint(1, 10)
        md5_maker = md5()
        pw = str(pw) + str(config.settings['cookie_secret']) + str(num)
        pw = pw.encode('utf-8')
        md5_maker.update(pw)
        return str(num) + "|" + md5_maker.hexdigest()

    @staticmethod
    def check_password(need_check_pw, old_pw):
        num = old_pw.split("|", 1)[0]
        older = old_pw.split("|", 1)[1]
        md5_maker = md5()
        need_check_pw = str(need_check_pw) + str(config.settings['cookie_secret']) + str(num)
        need_check_pw = need_check_pw.encode("utf-8")
        md5_maker.update(need_check_pw)
        if md5_maker.hexdigest() == older:
            return True
        else:
            return False

    @staticmethod
    def check_account(account):
        check_re = re.compile(r'\w{6,20}')
        re_match = re.match(check_re, account)
        if re_match:
            return True
        else:
            return False

    @staticmethod
    def single_login_token(account):
        num = random.randint(1, 10000)
        raw_token = str(account) + str(config.settings['cookie_secret']) + str(num)
        raw_token = raw_token.encode("utf-8")
        md5_maker = md5()
        md5_maker.update(raw_token)
        return md5_maker.hexdigest()
