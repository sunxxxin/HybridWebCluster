#-*- coding:utf-8 -*-
import Config
import datetime
from proto.general_pb2 import Mail
from proto.message_pb2 import Message
import ShopCfg
import json
import Service

def GetMoney(userid):
    strKey = Config.KEY_PACKAGE.format(userid=userid)
    money = 0
    if Config.grds.exists(strKey):
        money = int(Config.grds.hget(strKey, 'money'))
    else:
        result = Config.gdb.select('package', what="*", where="userid=$userid", vars=dict(userid=userid))
        if result:
            packageinfo = {
                'money': result[0]['money'],
                'coin': result[0]['coin'],
                'prop_1001': result[0]['prop_1001'],
                'prop_1002': result[0]['prop_1002'],
                'prop_1003': result[0]['prop_1003'],
                'prop_1006': result[0]['prop_1006'],
                'prop_1007': result[0]['prop_1007'],
                'freshtime': result[0]['freshtime'],
            }
            Config.grds.hmget(strKey, packageinfo)
            Config.grds.expire(strKey, 30 * 24 * 60 * 60)
            money = int(result[0]['money'])
    return money


def GetCoin(userid):
    strKey = Config.KEY_PACKAGE.format(userid=userid)
    if Config.grds.exists(strKey):
        coin = int(Config.grds.get(strKey, 'coin'))
    else:
        result = Config.gdb.select('package', what="*", where="userid=$userid", vars=dict(userid=userid))
    if result:
        packageinfo = {
            'money': result[0]['money'],
            'coin': result[0]['coin'],
            'prop_1001': result[0]['prop_1001'],
            'prop_1002': result[0]['prop_1002'],
            'prop_1003': result[0]['prop_1003'],
            'prop_1006': result[0]['prop_1006'],
            'prop_1007': result[0]['prop_1007'],
            'freshtime': result[0]['freshtime'],
        }
        Config.grds.hmget(strKey, packageinfo)
        Config.grds.expire(strKey, 30 * 24 * 60 * 60)
        coin = int(result[0]['coin'])
    return coin


def GetMonday(today):
    today = datetime.datetime.strptime(str(today), "%Y-%m-%d")
    return datetime.datetime.strftime(today - datetime.timedelta(today.weekday()), "%Y_%m_%d")

def sendMail(mailinfo):
    if not mailinfo:
        return 
    
    # type = '', date = '', title = '', context = '', attach = '', fromuserid = '', isglobal = ''
    mailproto = Mail()
    for userid in mailinfo['useridlist']:
        mailproto.userid.append(userid)
    mailproto.title = mailinfo['title']
    mailproto.type = mailinfo['type']
    mailproto.context = mailinfo['context']
    attach = {}
    for propid, propnum in mailinfo['attach'].items():
        if int(propid) in ShopCfg.SHOP_CFG:
            attach[propid] = propnum
    mailinfo.attach = json.dumps(attach)
    mailproto.getattach = 0
    mailproto.hasattach = 0

    if attach:
        mailproto.hasattach = 1

    # msg = Message()

    # 发送给邮件服务器
    Service.SendSvrd(Config.MAIL_HOST, Config.MAIL_PORT, mailproto.SerializePartialToString())

def GetGlobalMail(userid):
    pass

def GetMailList(userid):
    # 获取全服邮件


    # 拼邮件列表的key
    strKeyList = Config.KEY_MAIL_LIST.format(userid=userid)
    mailidlist = Config.grds.lrange(strKeyList, 0, -1)
    mailinfolist = []
    for mailid in mailidlist:
        strKey = Config.KEY_MAIL_DETAIL.format(mailid=mailid)
        result = Config.grds.hgetall(strKey)
        if not result:
            Config.grds.lrem(strKeyList, mailid, 0)
            continue
        mailinfo = {}
        mailinfo['mailid'] = mailid
        mailinfo['title'] = result['title']
        mailinfo['type'] = result['type']
        mailinfo['getattach'] = result['getattach']
        mailinfo['context'] = result['context']
        mailinfolist.append(mailinfo)
    return mailinfolist


def MailDelete(userid, mailid):
    strKeyList = Config.KEY_MAIL_LIST.format(userid=userid)
    Config.grds.lrem(strKeyList, mailid, 0)
    strKey = Config.KEY_MAIL_DETAIL.format(mailid=mailid)
    Config.grds.delete(strKey)

def MailDeleteAll(userid):
    strKeyList = Config.KEY_MAIL_LIST.format(userid=userid)
    mailidlist = Config.grds.lrange(strKeyList, 0, -1)
    for mailid in mailidlist:
        Config.grds.lrem(strKeyList, mailid, 0)
        strKey = Config.KEY_MAIL_DETAIL.format(mailid=mailid)
        Config.grds.delete(strKey)
    return {'code': 0}