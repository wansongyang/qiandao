import pymysql
from . import query
from . import utils
from . import utils as Info
from .globals import request
from .globals import session
from .router import Blueprint
from .query import DB

# 使用pymysql代替 mysqlclient
pymysql.install_as_MySQLdb()

def getConnect():
    from django.db import connection
    return connection

query.Configuration.init("",query.MysqlBuilder, connection=getConnect)

