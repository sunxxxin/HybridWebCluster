#-*- coding:utf-8 -*-
import web
import redis
DB_HOST = '192.168.3.223'
DB_PORT = 3306
DB_USER = 'sunxin'
DB_PW = '123456'
DB_NAME = 'classPy'

gdb = web.database(
    dbn = 'mysql',
    host = DB_HOST,
    port = DB_PORT,
    user = DB_USER,
    pw = DB_PW,
    db = DB_NAME
)

RDS_HOST = '127.0.0.1'
RDS_PORT = 6379
RDS_PW = '123456'

SESSION_EXPIRETIME = 30
LOGIN_INVALID_TIME = 30

grds = redis.Redis(
    host = RDS_HOST,
    port = RDS_PORT,
    password = RDS_PW
)
# grds.set('name', 'zhangsan')


DEFAULT_SECPASSWORD = '123456'

NEWUSER_DEFAULT_MONEY = 10000

USER_STATUS_NOLMAL = 0
USER_STATUS_FREEZE = 1

# 账号
KEY_PACKAGE = "KEY_PACKAGE_{userid}"
KEY_LOGIN = "KEY_LOGIN_{userid}"

MONEY_ID = 800
COIN_ID = 900

# 邮件
KEY_MAIL_LIST = "KEY_MAIL_LIST_{userid}"
KEY_MAIL_DETAIL = "KEY_MAIL_DETAIL_{mailid}"
MAIL_HOST = '127.0.0.1'
MAIL_PORT = 1234