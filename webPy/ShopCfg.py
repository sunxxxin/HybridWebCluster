#-*- coding:utf-8 -*-

# 商城版本号
SHOP_VERSION = 20240807124600

# 1 消耗型
# 2 时间型
TYPE_USE = 1
TYPE_TIME = 2

# 1 money
# 2 coin
TYPE_PAY_MONEY = 1
TYPE_PAY_COIN = 2

BUYLIMITTYPE_INVALID = 0
BUYLIMITTYPE_DAY = 1
BUYLIMITTYPE_WEEK = 2
BUYLIMITTYPE_MONTH = 3
BUYLIMITTYPE_YEAR = 4
 
ID_EXPCARD = 1001
ID_RANAMECARD = 1002
ID_GAMECLAERCARD = 1003
ID_YEARVIP_PACKGE = 1004
ID_MONTHVIP_PACKGE = 1005
ID_YEARVIP = 1006
ID_MONTHVIP = 1007


SHOP_LIST = [
        ID_EXPCARD,
        ID_RANAMECARD,
        ID_GAMECLAERCARD,
        ID_YEARVIP_PACKGE,
        ID_MONTHVIP_PACKGE,
]

SHOP_CFG = {
    ID_EXPCARD:{"pid": ID_EXPCARD, "name": "双倍经验卡", "type": TYPE_USE, "money": 100, 
            "coin": -1, "paytype": TYPE_PAY_MONEY, "iconid": 1001, "version": 10000, 
            "discount": 1, "inventory": -1, "buylimittype": BUYLIMITTYPE_INVALID, 
            "buylimitnum": -1, "proplist": [{"id": ID_EXPCARD, "num": 1}]},
            
    ID_RANAMECARD:{"pid": ID_RANAMECARD, "name": "改名卡", "type": TYPE_USE, "money": 100, 
            "coin": -1, "paytype": TYPE_PAY_MONEY, "iconid": 1002, "version": 10000, 
            "discount": 1, "inventory": -1, "buylimittype": BUYLIMITTYPE_INVALID, 
            "buylimitnum": -1, "proplist": [{"id": ID_RANAMECARD, "num": 1}]},

    ID_GAMECLAERCARD:{"pid": ID_GAMECLAERCARD, "name": "战绩清零卡", "type": TYPE_USE, "money": 100, 
            "coin": -1, "paytype": TYPE_PAY_MONEY, "iconid": 1003, "version": 10000, 
            "discount": 1, "inventory": -1, "buylimittype": BUYLIMITTYPE_INVALID, 
            "buylimitnum": -1, "proplist": [{"id": ID_GAMECLAERCARD, "num": 1}]},

    ID_YEARVIP_PACKGE:{"pid": ID_YEARVIP_PACKGE, "name": "年会员礼包", "type": TYPE_USE, "money": -1, 
            "coin": 1000, "paytype": TYPE_PAY_COIN, "iconid": 1004, "version": 10000, 
            "discount": 1, "inventory": -1, "buylimittype": BUYLIMITTYPE_INVALID, 
            "buylimitnum": -1, "proplist": [{"id": ID_YEARVIP, "num": 1}, {"id": ID_EXPCARD, "num": 10}, {"id": ID_RANAMECARD, "num": 10}]},

    ID_MONTHVIP_PACKGE:{"pid": ID_MONTHVIP_PACKGE, "name": "月会员礼包", "type": TYPE_USE, "money": -1, 
            "coin": 10, "paytype": TYPE_PAY_COIN, "iconid": 1005, "version": 10000, 
            "discount": 1, "inventory": -1, "buylimittype": BUYLIMITTYPE_INVALID, 
            "buylimitnum": -1, "proplist": [{"id": ID_MONTHVIP, "num": 1}, {"id": ID_EXPCARD, "num": 1}, {"id": ID_RANAMECARD, "num": 1}]},
}