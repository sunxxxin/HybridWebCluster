#-*- coding:utf-8 -*-

import ShopCfg
import ErrorCfg
import math
import Lobby
import Config
import DBManage
import datetime
import Account

def GetShopCfg(version):
    shop = ShopCfg.SHOP_LIST
    shoplist = []
    for id in shop:
        if id in ShopCfg.SHOP_CFG:
            cfg = ShopCfg.SHOP_CFG[id]
            if version < cfg['version']:
                continue
            proplist = {
                'pid': cfg['pid'], 'name': cfg['name'],
                'type': cfg['type'], 'money': cfg['money'], 'coin': cfg['coin'],
                'paytype': cfg['paytype'], 'iconid': cfg['iconid'], 'version': cfg['version'],
                'discount': cfg['discount'], 'inventory':cfg['inventory'], 'buylimittype': cfg['buylimittype'],
                'buylimitnum':cfg['buylimitnum'], 'proplist': cfg['proplist'],
            }
            shoplist.append(proplist)
    return {'shoplist': shoplist, 'shopversion': ShopCfg.SHOP_VERSION}

def ShopBuy(userid, propid, propnum, shopversion, version):
    # 判断商城版本号
    if int(shopversion) < ShopCfg.SHOP_VERSION:
        return {'code': ErrorCfg.EC_SHOP_VERSION_LOW, 'reason': ErrorCfg.ER_SHOP_VERSION_LOW}
    
    # 查看购买商品，校验版本号
    if int(propid) not in ShopCfg.SHOP_LIST:
        return{'code': ErrorCfg.EC_SHOP_BUY_LIST_NOT_EXIST, 'reason': ErrorCfg.ER_SHOP_BUY_LIST_NOT_EXIST}
    
    if not int(propid) in ShopCfg.SHOP_CFG:
        return {'code': ErrorCfg.EC_SHOP_BUY_PROP_NOT_EXIT, 'reason': ErrorCfg.ER_SHOP_BUY_PROP_NOT_EXIT}
    
    cfg = ShopCfg.SHOP_CFG[int(propid)]
    print('-----------------------')
    print(cfg)
    if cfg['version'] > int(version):
        return {'code': ErrorCfg.EC_SHOP_BUY_CLIENT_VERSION_LOW, 'reason': ErrorCfg.ER_SHOP_BUY_CLIENT_VERSION_LOW}
    
    # 计算购买数量是否大于购买数量，去缓存或数据库中取出剩余库存  （后续需要修改）
    # if int(propnum) > cfg['inventory']:
    #     return {'code': ErrorCfg.EC_SHOP_BUY_INVENIORY_NOT_ENOUGH, 'reason': ErrorCfg.ER_SHOP_BUY_INVENIORY_NOT_ENOUGH}
    




    # 购买
    if cfg['paytype'] == ShopCfg.TYPE_PAY_MONEY:
        needmoney = int(math.floor(cfg['money'] * cfg['discount'] * int(propnum)))
        result = PresentMoney(userid, -needmoney)
        if result['code'] != 0:
            return result
        money = result

    elif cfg['paytype'] == ShopCfg.TYPE_PAY_COIN:
        needcoin = int(math.floor(cfg['coin'] * cfg['discount'] * int(propnum)))
        coin = Lobby.GetCoin(userid)
        if coin < needcoin:
            return {'code': ErrorCfg.EC_SHOP_BUY_COIN_NOT_ENOUGH, 'reason': ErrorCfg.ER_SHOP_BUY_COIN_NOT_ENOUGH}
        
        strKey = Config.KEY_PACKAGE.format(userid=userid)

        coin = Config.grds.hincrby(strKey, 'coin', -needcoin)
        if coin < 0:
            Config.grds.hincrby(strKey, 'coin', +needcoin)
            return {'code': ErrorCfg.EC_SHOP_BUY_COIN_NOT_ENOUGH, 'reason': ErrorCfg.ER_SHOP_BUY_COIN_NOT_ENOUGH}
        now = datetime.datetime.now()
        DBManage.UpdateCoin(userid, coin, now)

    # 发货
    PresentProp(userid, propid, propnum)
    return {'code': 0, 'money': money}


def Present():
    # 遍历发送列表， 根据道具id，调用对应的函数发送奖励
    pass




def PresentMoney(userid, money):
    now = datetime.datetime.now()
    Account.InitPackage(userid, now)
    strKey = Config.KEY_PACKAGE.format(userid=userid)
    money = Config.grds.hincrby(strKey, 'money', -money)
    if money < 0:
        Config.grds.hincrby(strKey, 'money', +money)
        return {'code': ErrorCfg.EC_SHOP_BUY_MONEY_NOT_ENOUGH, 'reason': ErrorCfg.ER_SHOP_BUY_MONEY_NOT_ENOUGH}
    DBManage.UpdateMoney(userid, money, now)
    return {'code': 0, 'money': money}
        

def PresentProp(userid, propid, propnum):
    strKey = Config.KEY_PACKAGE.format(userid=userid)
    proplist = ShopCfg.SHOP_CFG[int(propid)]['proplist']
    now = datetime.datetime.now()
    propdict = {}
    for prop in proplist:
        propid = "prop_" + str(prop['id'])
        singlepropnum = Config.grds.hincrby(strKey,propid, prop['num'] * propnum)
        propdict[propid] = singlepropnum
    Config.grds.hset(strKey, 'freshtime', str(now))
    DBManage.UpdateProp(userid, propdict, now)
