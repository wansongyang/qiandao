from functools import wraps
from django.urls import path, include, re_path

# 路由装饰器类的实现，只需要在方法上 添加 @router.route('路径') 就能配置，省去了在urls.py 中配置的繁琐操作
class Blueprint:
    def __init__(self,name,url_prefix = ''):
        if len(url_prefix):
            url_prefix = url_prefix.strip('/') + '/'
        self.url_prefix = url_prefix
        self.name = name
        self.urls = []
        pass

    # 装饰器类
    def route(self,rule:str , name = None, methods = None):
        if name is None:
            name = rule.strip('/').replace('/','_')

        if rule != '':
            rule = rule.strip('/') + '/'

        def decorator( func ):
            self.add_rule(rule,func,name)
            # self.urls.append({
            #     path(rule, func ,name=name)
            # })
            return func

        return decorator

    # 添加规则
    def add_rule(self, rule, func, name):
        p =path(self.url_prefix+rule,func,name=name)
        self.urls.append(p)
        pass



#
# 这个是使用示例
# router = Blueprint("abc")
#
#
# @router.route('/index/')
# def index(request):
#     print("ccc")
#     pass
#
#
#
# if __name__ == '__main__':
#     index("bc")
