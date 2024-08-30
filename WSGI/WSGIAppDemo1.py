#-*- encoding:utf-8 -*-

from wsgiref.simple_server import make_server
import time
import sys
reload(sys) # type: ignore
sys.setdefaultencoding('utf-8')

class ResponseTimingMiddleware(object):
    def __init__(self, app):
        self.app = app 
    
    def __call__(self, env, start_response):
        start_time = time.time()
        response = self.app(env, start_response)
        response_time = (time.time() - start_time) * 1000
        timing_text = "记录请求耗时中间件输出\n\n本次请求耗时：{:.10f}ms \n\n\n".format(response_time)
        response.append(timing_text.encode('utf-8'))
        return response


def login(req):
    print(req)
    return req

def index(req):
    print(req)
    return req

def home(req):
    print(req)
    return req

pattern_url = {
    "/":home,
    "/login":login,
    "/index":index
}

def app(env, start_response):
    print(env.get('PATH_INFO'))

    url = env.get('PATH_INFO')
    params = env.get('QUERY_STRING')
    if url is None or url not in pattern_url.keys():
        start_response('404 not found', [('content-type', 'text/plain;charset=utf-8')])
        return[b'404 page not found']
    res = pattern_url.get(url)
    if res is None:
        start_response('404 not found', [('content-type', 'text/plain;charset=utf-8')])
        return[b'404 page not found']
    print('测试1------------------------------')
    start_response('200 Ok', [('content-type', 'text/plain;charset=utf-8')])
    print('测试2------------------------------')
    print('-------------' + params + '------------------')
    return [res(params).encode('utf-8')]

application = ResponseTimingMiddleware(app)
server = make_server('192.168.0.17', 8087, app= application)
# 启动服务
server.serve_forever()