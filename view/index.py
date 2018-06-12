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
        url = RequestHandler.reverse_url(self, "login")
        self.render("index/login.html", url=url)

    def post(self, *args, **kwargs):
        account = self.get_body_argument("account")
        if not Support.check_account(account):
            pass
            # TODO
        password = self.get_body_argument("password")
        db_checker = self.application.mongodb["user"]
        get_user = db_checker.find({"account": account})
        if len(get_user) == 0:
            pass
        if Support.check_password(password, get_user["password"]):
            pass
            # TODO
        else:
            pass
            # TODO
        print(account)
        print(password)
        self.render("index/login.html")


class RegisterHandler(RequestHandler):

    def get(self, *args, **kwargs):
        url = RequestHandler.reverse_url(self, "register")
        self.render("index/register.html", url=url)

    def post(self, *args, **kwargs):
        db_checker = self.application.mongodb["user"]
        account = self.get_body_argument("account", default=None, strip=True)
        get_user = db_checker.find({"account": account})
        if len(get_user) != 0 or not Support.check_account(account):
            pass
        password = self.get_body_argument("password", default=None, strip=True)
        confirm = self.get_body_argument("confirm", default=None, strip=True)
        if not password or not confirm:
            pass
            # TODO
        if password != confirm:
            pass
            # TODO
        email = self.get_body_argument("email", default=None, strip=True)
        get_email = db_checker.find({"email": email})
        self.render("index/register.html")


class Support(object):

    @staticmethod
    def get_password(pw):
        num = random.randint(1, 10)
        md5_maker = md5()
        pw = pw + config.settings['cookie_secret'] + str(num)
        md5_pw = md5_maker.update(pw).hexdigest()
        return str(num) + "|" + md5_pw

    @staticmethod
    def check_password(need_check_pw, old_pw):
        num = old_pw.split("|", 1)[0]
        older = old_pw.split("|", 1)[1]
        md5_maker = md5()
        need_check_pw = need_check_pw + config.settings['cookie_secret'] + str(num)
        check_pw = md5_maker.update(need_check_pw).hexdigest()
        if check_pw == older:
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
