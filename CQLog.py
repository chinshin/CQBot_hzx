# -*- coding: utf-8 -*-
import logging.handlers
import os

BASE_DIR = os.path.dirname(__file__)
LOG_FILE = os.path.join(BASE_DIR, 'CQBot.log')
# LOG_FILE = r'tst.log'

# handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1024 * 1024, backupCount=5, encoding='utf-8')  # 实例化handler
handler = logging.FileHandler(LOG_FILE)
fmt = '%(asctime)s - %(levelname)s - %(message)s'
# fmt = '%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s - %(message)s'

formatter = logging.Formatter(fmt)  # 实例化formatter
handler.setFormatter(formatter)  # 为handler添加formatter

logger = logging.getLogger('CQBot')  # 获取名为tst的logger
logger.addHandler(handler)  # 为logger添加handler
logger.setLevel(logging.DEBUG)


def INFO(*texts):
    msg = "\n"
    for text in texts:
        msg += str(text) + "\n"
    logger.info(msg)


def DEBUG(*texts):
    msg = "\n"
    for text in texts:
        msg += str(text) + "\n"
    logger.debug(msg)


def WARN(*texts):
    msg = "\n"
    for text in texts:
        msg += str(text) + "\n"
    logger.warn(msg)


def ERROR(*texts):
    msg = "\n"
    for text in texts:
        msg += str(text) + "\n"
    logger.error(msg, exc_info=True)


def CRITICAL(*texts):
    msg = "\n"
    for text in texts:
        msg += str(text) + "\n"
    logger.critical(msg)
