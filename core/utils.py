

from .query import DB, Model
from django.shortcuts import render
from .globals import request,session as sessionStore


def showMessage(code = 0,msg = '',href=None,replace = False):
    if href is None:
        href = request.headers.get("referer")
    return render(request,"message.html" , locals())

def showSuccess(msg ,href = None, replace = False):
    return showMessage(0,msg,href,replace)

def showError(msg,href='javascript:history.go(-1);',replace = False):
    return showMessage(1,msg,href,replace)

def session(name):
    return sessionStore.get(name)

def param(name:str,default = None) -> str:
    val = None
    if name in request.GET:
        val = request.GET.getlist(name)
    if name in request.POST:
        val = request.POST.getlist(name)
    if val is not None:
        return ",".join(val)
    return default

input=param

from objtyping import to_primitive
import json
def jsonEncode(root):
    v = to_primitive(root)
    return json.dumps(v,cls=DecimalEncoder)

def jsonDecode(string):
    return json.loads(string)

def checkLogin():
    username = sessionStore.get("username")
    if username is None or not len(username):
        return False
    return True

def checkLoginNot():
    return not checkLogin()

def paramlist(name:str,defs = None)->list:
    val = defs
    if name in request.GET:
        val = request.GET.getlist(name)
    if name in request.POST:
        val = request.POST.getlist(name)

    return val

inputlist=paramlist

import time as osTime
from datetime import datetime

def date(format,t=None):
    if t is None:
        t = osTime.time()
    if isinstance(t,type(datetime)):
        return t.strftime(format)
    if isinstance(t,int) or isinstance(t,float):
        return osTime.strftime(format, osTime.localtime(t))

    return datetime.now().strftime(format)

def time():
    return int(osTime.time())

def getDateStr():
    return date("%Y-%m-%d %H:%M:%S")

import random
def getID():
    a = random.randint(10000, 99999)
    return osTime.strftime("%y%m%d%H")+str(a)

def address(s):
    if s is None:
        return ''
    if not s:
        return ''
    add = json.loads(s)
    if isinstance(add,dict):
        if "address" in add:
            return add['address']
    return ''

def getAllChild(table,pid,value):
    templists = DB.name(table).select()
    return _getAllChild(pid,value,templists)

def _getAllChild(pid,value,templates):
    result = []
    parentid = value
    result.append(parentid)

    for child in templates:
        if child.get(pid) == parentid:
            ret = _getAllChild(pid,child.get("id"),templates)
            if len(ret):
                result += ret

    return result


def postion(table,pid,name,value):
    items = []
    parentid = value
    while(parentid):
        mp = DB.name(table).find(parentid)
        if not len(mp):
            break
        items.append(mp[name])
        parentid = mp.get(pid)

    items.reverse()
    return items

getTreeOption = postion



def images(s):
    if s is None:
        return ''

    s = str(s)
    arr = s.split(",")
    return arr[0]


def subStr(s,length,append = '...'):
    if s is None:
        return ''

    s = delHTMLTag(str(s))
    if len(s) > length:
        return s[0:length] + append
    return s

import re
def delHTMLTag(s):
    if s is None:
        return ''
    clean = re.compile('<.*?>')
    return re.sub(clean, '', s)

import html as osHtml
def html(content):
    if content is None:
        return ''
    return osHtml.escape(str(content))



import decimal
import datetime
from django.core.serializers.json import DjangoJSONEncoder
#import numpy as np
from django.db import models
from django.forms import model_to_dict

class DecimalEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        elif isinstance(o , datetime.datetime):
            return o.strftime("%Y-%m-%d %H:%M:%S")
        #if isinstance(o , int64):
        #elif isinstance(o, (np.integer, np.floating, np.bool_)):
        #    return o.item()
        #elif isinstance(o, np.ndarray):
        #    return o.tolist()
        elif isinstance(o,models.Model):
            return model_to_dict(o)
        else:
            return super().default(o)

def md5(obj:str):
    import hashlib
    f_md5 = hashlib.md5(obj.encode("utf-8"))
    return f_md5.hexdigest()


def getHash(username,pwd):
    zifuchuan = "{}+{}".format(username,pwd)
    return abs(hash_function(zifuchuan))


# 哈希函数
def hash_function(key):
    # 将字符串转换为ASCII值并求和作为散列结果
    result = sum([ord(char) for char in key]) % 100000
    return result




import math
class formatPage():
    def __init__(self, count, pagesize, currentPage=-1, pageTag='page', rollPage=2):
        self.count = count
        self.pagesize = pagesize
        self.pageCount = math.ceil(count / pagesize)
        self.pageTag = pageTag
        self.currentPage = currentPage
        self.rollPage = rollPage
        self.urlRule = self.createUrlRule()

    @property
    def hasNext(self):
        return self.currentPage < self.pageCount

    @property
    def hasPrev(self):
        return self.currentPage > 1

    @property
    def prevUrl(self):
        if self.hasPrev:
            return self.formatUrl(self.currentPage - 1)
        return ""

    @property
    def nextUrl(self):
        if self.hasNext:
            return self.formatUrl(self.currentPage + 1)
        return ""

    @property
    def firstUrl(self):
        return self.formatUrl(1)

    @property
    def lastUrl(self):
        return self.formatUrl(self.pageCount)

    def iter_pages(self) -> dict:
        start = 0
        end = 0
        rollPage = self.rollPage
        show_nums = rollPage * 2 + 1
        totalPages = self.pageCount
        currentPage = self.currentPage

        if totalPages < show_nums:
            start = 1
            end = totalPages
        elif currentPage < 1 + rollPage:
            start = 1
            end = show_nums
        elif currentPage >= (totalPages - rollPage):
            start = totalPages - show_nums
            end = totalPages
        else:
            start = currentPage - rollPage
            end = currentPage + rollPage

        result = {}
        while (start <= end):
            result[start] = self.formatUrl(start)
            start = start + 1

        return result

    @property
    def pageNums(self):
        return self.iter_pages().items()

    def formatUrl(self, page):
        return self.urlRule.replace("{page}", str(page), 1)

    def createUrlRule(self):
        path = request.path
        args = request.GET.copy()
        query = []
        for k, v in args.items():
            if k != self.pageTag:
                query.append("{}={}".format(k, v))
            else:
                if self.currentPage == -1:
                    self.currentPage = int(v)

        if self.currentPage == -1:
            self.currentPage = 1

        query.append(self.pageTag + "={page}")
        return path + "?" + ("&".join(query))