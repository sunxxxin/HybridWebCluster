#-*- coding:utf-8 -*-
from proto.message_pb2 import Message
from proto.general_pb2 import Sign
import ActionCfg
import Config
import MessageCfg
import TaskCfg
import Task
import datetime




def TaskMonitor():
    while True:
        strKey = ActionCfg.KEY_ACTION_TASK_LIST
        res = Config.grds.blpop(strKey)[1]
        msg = Message()
        msg.ParseFromString(res)
        msgid = int(msg.msgid) & MessageCfg.MSGID
        if msgid == MessageCfg.MSGID_SIGN:
            signinfo = Sign()
            signinfo.ParseFromString(msg.string)
            userid = int(signinfo.userid)
            date = signinfo.date
            for id in TaskCfg.TASK_LIST:
                cfg = TaskCfg.TASK_CFG[id]
                if cfg['action'] != ActionCfg.ACTION_SIGN:
                    continue
                datestr = datetime.datetime.strptime(str(date), "%Y-%m-%d")
                datestr = Task.GetTaskDatestr(cfg['type'], datestr)
                strKey = TaskCfg.KEY_TASK.format(userid=userid, date=datestr)
                if not Config.grds.exists(strKey):
                    Task.InitTaskCfg(userid, datestr)
                countfield = 'count_' + str(id)
                totalfield = 'total_' + str(id)
                statefield = 'state_' + str(id)
                count = Config.grds.hincrby(strKey, countfield, 1)
                result = Config.grds.hmget(strKey, statefield, totalfield)
                state = int(result[0])
                total = int(result[1])

                # 判断任务是否完成 
                if count >= total and state == TaskCfg.STATE_NOT_FINISH:
                    Config.grds.hset(strKey, statefield, TaskCfg.STATE_FINISH)
                    # 通知客户端
        elif msgid == MessageCfg.MSGID_LOGIN:
            pass


if __name__ == "__main__":
    TaskMonitor()