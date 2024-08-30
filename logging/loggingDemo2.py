#-*- coding:utf-8 -*-

import logging

# 高级用法

# 1.记录器
logger = logging.getLogger('applog')
print(logger.level)
print(logger)

logger.setLevel(logging.DEBUG)
print(logger.level)
print(logger)
print(type(logger))