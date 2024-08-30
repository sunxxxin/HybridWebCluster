#-*- coding:utf-8 -*-
import AccountCfg
import re
import Config
import datetime
import DBManage
import ErrorCfg

def CheckPhonenum(phonenum):
    #1.通过号段列表进行判断
    phonelist = [139, 138, 137, 136, 134, 135, 147, 150, 151, 152, 157, 158, 159, 172, 178,
         130, 131, 132, 140, 145, 146, 155, 156, 166, 185, 186, 175, 176, 196,
         133, 149, 153, 177, 173, 180, 181, 184, 189, 191, 193, 199,
         162, 165, 167, 170, 171]
    
    if len(phonenum) == 11 and str(phonenum).isdigit() and (int(phonenum[:3]) in phonelist):
        return True
    else:
        return False

def CheckUserIdNotRepeat(userid):
    # 检测账号是否重复，重复返回False，不重复返回True
    result = Config.gdb.select("user", where = "userid=$userid", vars=dict(userid=userid), what='count(*) as num')
    # Config.gdb.query("select count(*) as num from user where userid = {}".format(userid))
    if result and result[0].num >=1:
        return False
    return True

# 检测身份证号
def CheckIdCard(idcard):
    """
    检查身份证号码是否合理
     
    参数:
    idcard (str): 18位身份证号码
   
    返回:
    bool: True 表示身份证号码合理, False 表示身份证号码不合理
    """
    stridcard = str(idcard)
    # 地区检验
    if (stridcard)[0:2] not in AccountCfg.AREAID:
        return False

    # 检查长度是否为18位
    if len(idcard) != 18:
        return False

    # 检查前17位是否全部为数字
    if not idcard[:17].isdigit():
        return False

    # 计算校验码
    factors = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    check_sum = sum([int(idcard[i]) * factors[i] for i in range(17)]) % 11
    check_codes = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']
    if idcard[17] != check_codes[check_sum]:
        return False

    # 检查出生日期是否合法
    try:
        year = int(idcard[6:10])
        month = int(idcard[10:12])
        day = int(idcard[12:14])
        if year < 1900 or year > 2100 or month < 1 or month > 12 or day < 1 or day > 31:
            return False
    except ValueError:
        return False
    return True

def CheckPassword(password):
    # 字母和数字组合，8-16位
    print('CheckPassword测试')
    print(password)
    pattern = re.compile('^(?=.*[0-9])(?=.*[A-z])[0-9a-zA-Z]{8,16}$')
    if re.match(pattern, password):
        return True
    return False

def InitPackage(userid, now):
    # 初始化用户背包
    strKey = Config.KEY_PACKAGE.format(userid=userid)
    if Config.grds.exists(strKey):
        return 
    else:
        result = Config.gdb.select('package', what="*", where="userid=$userid", vars=dict(userid=userid))
        if result:
            packageinfo = {}
            for k, v in result[0].items():
                packageinfo[k] = v
            Config.grds.hmget(strKey, packageinfo)
            Config.grds.expire(strKey, 30 * 24 * 60 * 60)
        else:
            packageinfo = {
                'money': Config.NEWUSER_DEFAULT_MONEY,
                'coin': 0,
                'prop_1001': 0,
                'prop_1002': 0,
                'prop_1003': 0,
                'prop_1006': 0,
                'prop_1007': 0,
                'freshtime': str(now),
            }
            Config.grds.hmset(strKey, packageinfo)
            Config.grds.expire(strKey, 30 * 24 * 60 * 60)
            packageinfo['userid'] = userid
            DBManage.InitPackage(packageinfo)


def InitUser(phonenum, password, nick, sex, idcard):
    now = datetime.datetime.now()
    DBManage.InsertRegisterUser(phonenum, password, nick, sex, idcard, now)
    InitPackage(phonenum, now)


def VerifyAccount(userid, password):
    result = Config.gdb.select("user", what = "password, status", vars = dict(userid=userid), where = "userid=$userid")
    print(type(result))
    if not result:
        return {'code':ErrorCfg.EC_LOGIN_USERID_ERROR, 'reason':ErrorCfg.ER_LOGIN_USERID_ERROR}
    res = result[0]
    if res['password'] != password:
        return {'code':ErrorCfg.EC_LOGIN_PASSWORD_ERROR, 'reason':ErrorCfg.ER_LOGIN_PASSWORD_ERROR}
    if res['status'] != Config.USER_STATUS_NOLMAL:
        pass
    return {'code':0}



def HandleLogin(userid, session):
    now = datetime.datetime.now()
    session['userid'] = userid
    logininfo = {
        'freshtime': str(now),

    }
    print('+++++++++++++++++++++++++')
    print(session)
    Config.grds.hmset(Config.KEY_LOGIN.format(userid=userid), logininfo)
    Config.grds.expire(Config.KEY_LOGIN.format(userid=userid), Config.LOGIN_INVALID_TIME)
    Config.gdb.update(
        "user",
        lastlogintime = now,
        where = "userid=$userid",
        vars = dict(userid = userid)
    )
    return {'code': 0}