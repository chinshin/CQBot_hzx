# -*- coding: utf-8 -*-
import logging.handlers
import os

BASE_DIR = os.path.dirname(__file__)
LOG_FILE = os.path.join(BASE_DIR, 'tst.log')
# LOG_FILE = r'tst.log'

handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1024 * 1024, backupCount=5, encoding='utf-8')  # 实例化handler
fmt = '%(asctime)s - %(levelname)s - %(message)s'
# fmt = '%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s - %(message)s'

formatter = logging.Formatter(fmt)  # 实例化formatter
handler.setFormatter(formatter)  # 为handler添加formatter

logger = logging.getLogger('tst')  # 获取名为tst的logger
logger.addHandler(handler)  # 为logger添加handler
logger.setLevel(logging.DEBUG)


def INFO(text):
    logger.info(str(text))


def DEBUG(text):
    logger.debug(str(text))


def WARN(text):
    logger.warn(str(text))


def ERROR(text):
    logger.error(str(text), exc_info=True)


def CRITICAL(text):
    logger.critical(str(text))
