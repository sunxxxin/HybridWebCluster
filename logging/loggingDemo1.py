#-*- coding:utf-8 -*-

import logging

# 默认的日志输出级别为warning

logging.basicConfig(level=logging.DEBUG, filename='', filemode='w') # 设置日志输出级别

logging.debug("This is debug log")
logging.info("This is info log")
logging.warning("This is warning log")
logging.error("This is error log")
logging.critical("This is critical log")