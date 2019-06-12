# -*- coding: utf-8 -*-
import os


def get_logfile(name):
    return os.path.join(os.path.dirname(__file__), name)
