#-*- coding:utf-8 -*-
import logging.config
import web
import Account
import json
import ErrorCfg
import Error
import Config
import logging
import Shop
from RedisStore import RedisStore
import Task
import Lobby

urls = (
    '/register', 'Register',
    '/login', 'Login',
    '/shop/cfg', 'Shop_cfg',
    '/shop/buy', 'Shop_buy',
    '/task/cfg', 'Task_cfg',
    'task/reward', 'Task_reward',
    '/sign', 'Sign',
    '/mail/send', 'Mail_send',
    '/mail/list', 'Mail_list',
    '/mail/delete', 'Mail_delete',
    '/mail/getattach', 'Mail_getattach',
    '.mail/delete/all', 'Mail_delete_all',

)

app = web.application(urls, globals())
application = app.wsgifunc() 



logging.config.fileConfig('logging.conf')
logger = logging.getLogger('applog')


if web.config.get('_session') is None:
    session = web.session.Session(app, RedisStore(Config.grds, Config.SESSION_EXPIRETIME))
    web.config._session = session
else:
    session = web.config._session


def CatchError(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.exception(e)
    return wrapper

def CheckLogin(func):
    def wrapper(*args, **kwargs):
        if 'userid' in session.__dict__:
            return func(*args, **kwargs)
        else:
            return Error.ErrResult(ErrorCfg.EC_LOGIN_INVALID, ErrorCfg.ER_LOGIN_INVALID)
    return wrapper
    

class Register:
    @CatchError
    def POST(self):
        req = web.input(phonenum = '', password = '', nick = '', sex = '', idcard = '')
        phonenum = req.phonenum
        password = req.password
        nick = req.nick
        sex = req.sex
        idcard = req.idcard
        
        # 检测手机号格式
        if not Account.CheckPhonenum(phonenum):
            return Error.ErrResult(ErrorCfg.EC_REGISTER_PHONENUM_TYPE_ERROR, ErrorCfg.ER_REGISTER_PHONENUM_TYPE_ERROR)

        
        # 检测账号是否重复
        if not Account.CheckUserIdNotRepeat(phonenum):
            return Error.ErrResult(ErrorCfg.EC_REGISTER_USERID_REPEAT, ErrorCfg.ER_REGISTER_USERID_REPEAT)
        
        # 检测身份证格式
        if not Account.CheckIdCard(idcard):
            return Error.ErrResult(ErrorCfg.EC_REGISTER_IDCARD_TYPE_ERROR, ErrorCfg.ER_REGISTER_IDCARD_TYPE_ERROR)
        
        # 检测密码格式
        if not Account.CheckPassword(password):
            print('Account.CheckPassword测试')
            print(password)
            return Error.ErrResult(ErrorCfg.EC_REGISTER_PASSWORD_TYPE_ERROR, ErrorCfg.ER_REGISTER_PASSWORD_TYPE_ERROR)
        
        # 注册账号
        Account.InitUser(phonenum, password, nick, sex, idcard)
        return json.dumps({'code':0})
    
class Login:
    @CatchError
    def POST(self):
        req = web.input(userid = '', password = '')
        userid = req.userid
        password = req.password

        result = Account.VerifyAccount(userid, password)
        if result['code'] != 0:
            return Error.ErrResult(result['code'], result['reason'])
        # 登录处理
        result = Account.HandleLogin(userid, session)
        if result['code'] != 0:
            return Error.ErrResult(result['code'], result['reason'])
        return json.dumps({'code':0})

class Shop_cfg:
    @CatchError
    @CheckLogin
    def GET(self):
        req = web.input(version = '')
        version = int(req.version)
        shopcfg = Shop.GetShopCfg(version)
        return json.dumps({'code': 0, 'shopcfg': shopcfg})

class Shop_buy:
    @CatchError
    @CheckLogin
    def POST(self):
        req = web.input(userid = '', propid = '', propnum = '', shopversion = '', version = '')
        userid = req.userid
        propid = req.propid
        propnum = req.propnum
        shopversion = req.shopversion
        version = req.version
        dictInfo = Shop.ShopBuy(userid, propid, propnum, shopversion, version)
        
        return json.dumps(dictInfo)


class Task_cfg:
    @CatchError
    @CheckLogin
    def GET(self):
        req = web.input(userid = '', version = '')
        userid = int(req.userid)
        version = int(req.version)
        taskcfg = Task.GetTaskCfg(userid, version)
        return json.dumps({'code': 0, 'taskcfg': taskcfg})
    

class Task_reward:
    @CatchError
    @CheckLogin
    def POST(self):
        req = web.input(userid = '', taskid = '')
        userid = int(req.userid)
        taskid = int(req.taskid)
        result = Task.TaskReward(userid, taskid)
        if result['code'] != 0:
            return Error.ErrResult(result['code'], result['reason'])
        return json.dumps({'code': 0})
    


class Sign:
    @CatchError
    @CheckLogin
    def POST(self):
        req = web.input(userid = '', signtype = '', date = '')
        userid = int(req.userid)
        signtype = int(req.signtype)
        date = req.date
        Task.UserSign(userid, signtype, date)
        return json.dumps({'code': 0})
    


class Mail_send:
    @CatchError
    @CheckLogin
    def POST(self):
        req = web.input(useridlist = '', type = '', date = '', title = '', context = '', attach = '', fromuserid = '', isglobal = '')
        req.useridlist = map(int, req.useridlist.split(','))
        req.attach = json.loads(req.attach)
        Lobby.sendMail(req)
        return json.dumps({'code': 0})
    
class Mail_list:
    @CatchError
    @CheckLogin
    def POST(self):
        req = web.input(userid = '')
        userid = int(req.userid)
        mailinfolist = Lobby.GetMailList(userid)


        return json.dumps({'code': 0, 'mailinfolist': mailinfolist})


class Mail_delete:
    @CatchError
    @CheckLogin
    def POST(self):
        req = web.input(userid = '', mailid = '')
        userid = int(req.userid)
        mailid = req.mailid
        Lobby.MailDelete(userid, mailid)


        return json.dumps({'code': 0})
    

class Mail_delete_all:
    @CatchError
    @CheckLogin
    def POST(self):
        req = web.input(userid = '')
        userid = int(req.userid)
        Lobby.MailDeleteAll(userid)


        return json.dumps({'code': 0})



# if __name__ == '__main__':
#     app.run()