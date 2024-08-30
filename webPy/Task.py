#-*- coding:utf-8 -*-

import TaskCfg
import Config
import datetime
import json
import Lobby
import Shop
import ErrorCfg
from proto.general_pb2 import Sign
import Action
import MessageCfg

def InitTaskCfg(userid, datestr):
    taskinfo = {} 
    strKey = TaskCfg.KEY_TASK.format(userid=userid, date=datestr)
    for id in TaskCfg.TASK_LIST:
         if id in TaskCfg.TASK_CFG:
            cfg = TaskCfg.TASK_CFG[id]
            taskinfo['count_' + str(id)] = 0
            taskinfo['total_' + str(id)] = cfg['total']
            taskinfo['state_' + str(id)] = TaskCfg.STATE_NOT_FINISH
            taskinfo['reward_' + str(id)] = json.dumps(cfg['rewardlist'])
    Config.grds.hset(strKey, mapping=taskinfo)


# 优化，根据任务id，选择性初始化任务配置，减少内存占用
def InitTaskCfgByField(userid, taskid, datestr):
    pass


def GetTaskDatestr(type, today):
    if type == TaskCfg.TYPE_WEEK:
        datestr = Lobby.GetMonday(today)
    elif type == TaskCfg.TYPE_MONTH:
        datestr = str(today.year) + "_" + str(today.month) + "_1"
    elif type == TaskCfg.TYPE_YEAR:
        datestr = str(today.year) + "_1_1"
    else:
        datestr = today.strftime("%Y_%m_%d")
    return datestr


def GetTaskCfg(userid, version):
    task = TaskCfg.TASK_LIST
    tasklist = []
    now = datetime.date.today()
    datestr = now.strftime("%Y_%m_%d")
    strKey = TaskCfg.KEY_TASK.format(userid=userid, date=datestr)
    if not Config.grds.exists(strKey):
        InitTaskCfg(userid, datestr)
    for id in task:
        if id in TaskCfg.TASK_CFG:
            cfg = TaskCfg.TASK_CFG[id]
            if version < cfg['version']:
                continue
            taskdict = {
                'tid': cfg['tid'], 'type': cfg['type'], 'iconid': cfg['iconid'], 'series': cfg['series'], 
                'name': cfg['name'], 'desc': cfg['desc'], 'total': cfg['total'], 'version': cfg['version'], 
                'rewardlist':cfg['rewardlist'], 'count': 0, 
            }
            datestr = GetTaskDatestr(cfg['type'], now)
            strKey = TaskCfg.KEY_TASK.format(userid=userid, date=datestr)
            taskinfo = Config.grds.hgetall(strKey)
            if taskinfo:
                countfield = 'count_' + str(id)
                statefield = 'state_' + str(id)
                taskdict['count'] = taskinfo[countfield] if countfield in taskinfo else 0
                taskdict['state'] = taskinfo[statefield] if statefield in taskinfo else TaskCfg.STATE_INVALID

            tasklist.append(taskdict)
    return {'tasklist': tasklist}


def TaskReward(userid, taskid): # 任务奖励
     # 判断任务id是否合法
    if taskid not in TaskCfg.TASK_LIST:
        return {'code': ErrorCfg.EC_TASK_ID_INVALID, 'reason': ErrorCfg.ER_TASK_ID_INVALID}

    # 判断用户是否完成任务
    now = datetime.datetime.today()
    cfg = TaskCfg.TASK_CFG['taskid']
    datestr = GetTaskDatestr(cfg['type'], now)
    strKey = TaskCfg.KEY_TASK.format(userid = userid, date = datestr)

    statefield = 'state_' + str(taskid)
    state = Config.grds.hget(strKey, statefield)
    if state != TaskCfg.STATE_FINISH:
        return {'code': ErrorCfg.EC_TASK_NOT_FINISTH, 'reason': ErrorCfg.ER_TASK_NOT_FINISTH}
     
    # 发奖励 Present
    rewardfield = 'reward_' + str(taskid)
    rewardlist = Config.grds.hget(strKey, rewardfield)
    rewardlist = json.loads(rewardlist)
    money = 0
    for reward in rewardlist:
        currencytype = reward['id']
        num = reward['num']
        if currencytype == Config.MONEY_ID:
            money += num

    Shop.PresentMoney(userid, money)
    return {'code': 0, 'money': money}


def UserSign(userid, signtype, date):
    if signtype == TaskCfg.SIGN_TYPE_TODAY:
        date = datetime.datetime.today()
    elif signtype == TaskCfg.SIGN_TYPE_AGO:
        date = datetime.datetime.strptime(str(date), "%Y_%m_%d")
    else:
        return {'code':ErrorCfg.EC_TASK_SIGN_TYPE_ERROR, 'reason':ErrorCfg.ER_TASK_SIGN_TYPE_ERROR}
    
    day = date.day
    month_firstday = str(date.year + '_' + str(date.month) + '_1')
    strKey = TaskCfg.KEY_SIGN.format(userid=userid, date=month_firstday)
    Config.grds.setbit(strKey, day, 1)


    # 发送签到事件
    signproto = Sign()
    signproto.userid = userid
    signproto.signtype = signtype
    signproto.date = date.strftime("%Y_%m_%d")
    Action.SendAction(userid, MessageCfg.MSGID_SIGN, signproto.SerializePartialToString())