from django.http import HttpRequest, HttpResponse
from django.utils.deprecation import MiddlewareMixin
from werkzeug.local import LocalStack

from .ctx import RequestContext
from .globals import _cv_request

# 当前生命周期的代理对象设置
class MiddlewareProxy(MiddlewareMixin):
    def __init__(self,get_response):
        super().__init__(get_response)

    def process_request(self,request:HttpRequest):
        request.requestCtx = RequestContext(request)
        request.requestCtx.push()
        pass

    def process_response(self,request:HttpRequest,response:HttpResponse):
        request.requestCtx.pop()
        return response

