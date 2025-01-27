#-*- coding:utf-8 -*-
import Config
import ActionCfg

KEY_TASK = "KEY_TASK_{userid}_{date}"

ID_INVALID = -1
ID_SIGN = 20001
ID_SIGN_SEVENDAYS = 20002
ID_PLAY_SERIES_1 = 20003
ID_PLAY_SERIES_2 = 20004
ID_PLAY_SERIES_3 = 20005



TYPE_DAY = 1
TYPE_WEEK = 2
TYPE_MONTH = 3
TYPE_YEAR = 4


TASK_LIST = {
    ID_SIGN,
    ID_SIGN_SEVENDAYS,
    ID_PLAY_SERIES_1,
    ID_PLAY_SERIES_2,
    ID_PLAY_SERIES_3,
}


STATE_INVALID = -1
STATE_NOT_FINISH = 1
STATE_FINISH = 2
STATE_AWARDED = 3



# 签到
KEY_SIGN = "KEY_SIGN_{userid}_{date}"
SIGN_TYPE_TODAY = 1
SIGN_TYPE_AGO = 2

TASK_CFG = {
    ID_SIGN:{'tid': ID_SIGN, 'type': TYPE_DAY, 'action': ActionCfg.ACTION_SIGN, 'iconid': 20001, 'series': ID_INVALID, 
             'name': "每日签到", 'desc': "每日签到后领取奖励", 'total': 1, 'version': 10000, 
             'rewardlist':[{'id': Config.MONEY_ID, 'num': 1000}]},

    ID_SIGN_SEVENDAYS:{'tid': ID_SIGN_SEVENDAYS, 'type': TYPE_WEEK, 'action': ActionCfg.ACTION_SIGN, 'iconid': 20002, 'series': ID_INVALID, 
             'name': "每周签到", 'desc': "每周签到7天后领取奖励", 'total': 7, 'version': 10000, 
             'rewardlist':[{'id': Config.MONEY_ID, 'num': 10000}]},

    ID_PLAY_SERIES_1:{'tid': ID_PLAY_SERIES_1, 'type': TYPE_DAY, 'action': ActionCfg.ACTION_PLAY, 'iconid': 20003, 'series': ID_INVALID, 
             'name': "每日对局5场", 'desc': "每日对局5场后领取奖励", 'total': 5, 'version': 10000, 
             'rewardlist':[{'id': Config.MONEY_ID, 'num': 5000}]},

    ID_PLAY_SERIES_2:{'tid': ID_PLAY_SERIES_2, 'type': TYPE_DAY, 'action': ActionCfg.ACTION_PLAY, 'iconid': 20004, 'series': ID_PLAY_SERIES_1, 
             'name': "每日对局10场", 'desc': "每日对局10场后领取奖励", 'total': 10, 'version': 10000, 
             'rewardlist':[{'id': Config.MONEY_ID, 'num': 10000}]},

    ID_PLAY_SERIES_3:{'tid': ID_PLAY_SERIES_3, 'type': TYPE_DAY, 'action': ActionCfg.ACTION_PLAY, 'iconid': 20005, 'series': ID_PLAY_SERIES_2, 
             'name': "每日对局20场", 'desc': "每日对局20场后领取奖励", 'total': 20, 'version': 10000, 
             'rewardlist':[{'id': Config.MONEY_ID, 'num': 20000}]},
}