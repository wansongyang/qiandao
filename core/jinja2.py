import json

from django.contrib.sessions.backends.base import SessionBase
from django.http import QueryDict
from django.templatetags.static import static
from django.urls import reverse
from .query import DB
from jinja2 import Environment
from . import utils

# 配置空对象、session QueryDict，类的处理对象
def finalize(value):
    if value is None:
        return ''
    if isinstance(value,QueryDict):
        return json.dumps(value.dict())

    if isinstance(value,SessionBase):
        return ''

    #print("finalize {}".format(value))
    return str(value)

# 空字符串的时候不显示None
def undefinedfinalize(obj=None,name = None):
    if obj is None:
        return ''
    return ''


# 配置jinja2 模板引擎的相关参数
def environment(**options):
    env = Environment(**options)
    env.globals.update(
        {
            "static": static,
            "url": reverse,
            'DB': DB,
            'Info': utils,
            'utils': utils,
        }
    )

    env.autoescape = False
    env.finalize = finalize

    env.undefined = undefinedfinalize
    return env