# -*- coding: utf-8 -*-
import sys
import time
import logging

from Log import get_logfile


def set_logging(part):
    this_logger = logging.getLogger(part)
    this_logger.setLevel(logging.INFO)
    rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
    log_name = part + rq + '.log'
    logfile = get_logfile(log_name)
    fh = logging.FileHandler(logfile, mode='w', encoding='UTF-8')
    fh.setLevel(logging.INFO)
    sh = logging.StreamHandler(sys.stdout)
    sh.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
    fh.setFormatter(formatter)
    sh.setFormatter(formatter)
    this_logger.addHandler(fh)
    this_logger.addHandler(sh)
    this_logger.info('启动' + part + '记录器')
    return this_logger

