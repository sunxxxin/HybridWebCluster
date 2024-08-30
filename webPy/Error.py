#-*- coding:utf-8 -*-
import json


def ErrResult(code, reson):
    return json.dumps({'code': code, 'reson': reson})