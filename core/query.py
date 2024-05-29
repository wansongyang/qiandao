
# 数据库的参数设置
class QueryOptions():

    name=''
    options = {}
    def __init__(self,name):
        self.name = name
        self.options = {}

    # 设置字段
    def field(self,field = '*'):
        fields = self.getOptionArray("field")
        fields.append(field)
        return self

    # 设置获取行数
    def limit(self,offset,nLimit = None):
        if isinstance(offset,str):
            if offset.find(',') != -1:
                arr = offset.split(",")
                offset = arr[0]
                nLimit = arr[1]

        if not nLimit:
            nLimit = offset
            offset = 0

        v = self.getOptionObject("limit")
        v["offset"] = offset
        v["size"] = nLimit

        return self

    # 设置分组
    def group(self,group):
        self.getOptionArray("group").append(group)
        return self

    # 设置排序
    def order(self,orderby , sort = None):
        if sort is not None:
            orderby = orderby + " "+ sort

        self.getOptionArray("order").append(orderby)
        return self

    def orderAsc(self,field):
        return self.order(field,"asc")

    def orderDesc(self,field):
        return self.order(field,"desc")

    def join(self,table,cond,type = ''):
        sql = " {} JOIN {} ON {} ".format(type,table,cond)
        self.getOptionArray("join").append(sql)
        return self

    def joinLeft(self,table,cond):
        return self.join(table,cond,"LEFT")

    def joinRight(self,table,cond):
        return self.join(table, cond, "RIGHT")

    def joinInner(self,table,cond):
        return self.join(table, cond, "INNER")

    def alias(self , alias ):
        self.options["alias"] =alias
        return self

    def where(self,field=None , exp = None,cond = None , like = 'AND' ,*args,**kwargs):
        if field is not None:
            wheres = self.getOptionArray('where')
            raw = False
            if exp is None and cond is None:
                raw = True
            elif cond is None:
                cond = exp
                exp = '='
            wheres.append({
                'name':field,
                'exp':exp,
                'value':cond,
                'connect':like,
                'raw':raw
            })
        if len(kwargs):
            for k, v in kwargs.items():
                if isinstance(v,list) or isinstance(v,tuple):
                    self.where(k,v[0],v[1])
                else:
                    self.where(k, '=', v)
        return self

    def whereLike(self,field,val):
        return self.where(field,"like" , val)

    def whereLikeNot(self,field,val):
        return self.where(field, "not like", val)

    def whereIn(self,field,val):
        return self.where(field, "in", val)

    def whereInNot(self,field,val):
        return self.where(field, "not in", val)

    def whereBetween(self,field,start,end = None):
        val = []
        if end is None:
            val = start.split(",")
        else:
            val.append(start)
            val.append(end)

        return self.where(field, "between", val)

    def whereBetweenNot(self,field,start,end = None):
        val = []
        if end is None:
            val = start.split(",")
        else:
            val.append(start)
            val.append(end)

        return self.where(field, "not between", val)


    def getOptionArray(self,name) -> list:
        if name in self.options:
            return self.options[name]
        self.options[name] = []
        return self.options[name]

    def getOptionObject(self,name) -> dict:
        if name in self.options:
            return self.options[name]
        self.options[name] = {}
        return self.options[name]


class Query(QueryOptions):
    _data = {}
    pk='id'
    def __init__(self,name,pk='id'):
        super(Query, self).__init__(name)
        self._data = {}
        self.pk = pk


    def data(self,name=None,value = None , **kwargs):
        if name is not None:
            if isinstance(name,dict):
                for k,v in name.items():
                    self._data[k] = v
                #self._data.update(name)
            else:
                self._data[name] = value

        if len(kwargs):
            self._data.update(kwargs)

        return self

    def getData(self,name=None):
        if name is None:
            return self._data
        elif name in self._data:
            return self._data[name]
        else:
            return None

    def inc(self,name,step=1):
        return self.data(name,['inc',step])

    def dec(self,name,step):
        return self.data(name,['dec',step])

    def setField(self,name,value):
        return self.data(name,value).update()

    def setInc(self,name,step=1):
        return self.inc(name,step).update()

    def setDec(self,name,step=1):
        return self.dec(name, step).update()

    def count(self):
        return self.total('count','0')

    def max(self,field):
        return self.total('max',field)

    def sum(self,field):
        return self.total('sum',field)

    def min(self,field):
        return self.total('min',field)

    def avg(self,field):
        return self.total('avg',field)





    def total(self,func,field):
        import copy
        options = copy.deepcopy(self.options)
        c = Query(self.name, self.pk)
        c.options = options
        fields = c.getOptionArray('field')
        fields.clear()
        c.field('{}({}) count'.format(func,field))
        row = c.find()
        return row.count if row.count is not None else 0

    def paginate(self,page=1,pagesize = 12) -> tuple:
        builder = Configuration.getBuilder(self)
        count = self.count()
        page = int(page)
        self.limit((page-1)*pagesize , pagesize)
        sql = builder.builderSelect()
        lists = DB.select(sql)

        return count,lists

    def select(self):
        builder = Configuration.getBuilder(self)
        sql = builder.builderSelect()
        lists = DB.select(sql)
        return lists

    def find(self,id = None):
        if id is not None:
            self.where(self.pk,id)

        builder = Configuration.getBuilder(self)
        sql = builder.builderSelect()
        return DB.find(sql,self.name)

    def column(self,field:str,key=None):
        if "field" not in self.options:
            self.field(field)
            if key is not None:
                self.field(key)

        isMulField = field.find(",") != -1
        lists = self.select()
        if key is None:
            if isMulField:
                return lists
            else:
                result = []
                for v in lists:
                    if field in v:
                        result.append(v[field])

                return result
        else:
            result = {}
            if isMulField:
                for v in lists:
                    result[v[key]] = v
            else:
                for v in lists:
                    result[v[key]] = v[field]

            return result

    def update(self,data = None):
        if data is not None:
            self.data(data)

        if "where" not in self.options:
            if self.pk in self._data:
                self.where(self.pk,self._data[self.pk])
            else:
                return False

        builder = Configuration.getBuilder(self)
        sql = builder.builderUpdate()
        DB.execute(sql)
        return True

    def insert(self,data = None , isReplace = False):
        if data is not None:
            self.data(data)

        builder = Configuration.getBuilder(self)
        sql = builder.builderInsert(isReplace)
        return DB.execute(sql)


class Model(dict):
    def __init__(self, table , data=None, update=True):
        if data is not None:
            super(Model, self).__init__(data)
        if table is not None:
            self.__table = table
        self.__update = update
        self.__index = 0
        self.__keys = []

    def __repr__(self):
        result = []
        for key in self.keys():
            v = self[key]
            if isinstance(v,bool):
                if v:
                    v = "true"
                else:
                    v = "false"
            elif not (isinstance(v,int) or isinstance(v,float)):
                v = "\"{}\"".format(v)

            result.append("\"{}\":{}".format(key,v))

        return "{"+(",".join(result))+"}"


    def __getattr__(self, item):
        # print('called " __getattr__" ')
        if item in self:
            return self[item]
        if item in self.__dict__:
            return self.__dict__[item]
        return None

    def __setattr__(self, key, value):
        # print('called __setattr__ key {} value {}'.format(key,value))
        if key in self.__dict__:
            self.__dict__[key] = value
        else:
            self[key] = value

    def __iter__(self):
        self.__index = 0
        self.__keys = self.keys()
        return iter(self.__keys)

    def __next__(self):
        if self.__index < len(self.__keys):
            self.__index += 1
            return self.__keys[self.__index]
        else:
            raise StopIteration

    def __len__(self):
        return len(self.keys())

    def isReturn(self, name):
        if name.find('_Model') == -1 and (name.find('__') == -1 or name.find('__') > 0):
            return True
        return False

    def items(self):
        for k, v in super(Model, self).items():
            if self.isReturn(k):
                yield k, v

    def keys(self):
        result = []
        for k, v in super(Model, self).items():
            if self.isReturn(k):
                result.append(k)
        return result

    def values(self):
        result = []
        for k, v in super(Model, self).items():
            if self.isReturn(k):
                result.append(v)
        return result

    def save(self):
        print("table {} save {}".format(self['__table'],self))
        if self.__update:
            DB.name(self['__table']).data(self).update()
        else:
            self.id = DB.name(self['__table']).data(self).insert()

class ConnectionIntfer:
    def __init__(self,connection):
        self.connection = connection

    def select(self,sql,name=None,echo=True):
        raise NotImplementedError('为继承该方法')

    def find(self, sql, name=None, echo=True):
        raise NotImplementedError('为继承该方法')

    def findOne(self, sql, echo=True):
        raise NotImplementedError('为继承该方法')

    def execute(self, sql, echo=True):
        raise NotImplementedError('为继承该方法')

import logging

class RawConnection(ConnectionIntfer):
    def __init__(self,connection):
        super(RawConnection, self).__init__(connection)

    def select(self,sql,name=None,echo=True):
        cursor = None
        result = []
        try:
            if echo:
                print(sql)
                #print(sql)
            cursor = self.connection.cursor()
            reCount = cursor.execute(sql)
            col_names = [row[0] for row in cursor.description]
            if reCount:
                alls = cursor.fetchall()
                for v in alls:
                    re = Model(data=zip(col_names, v), table=name)
                    result.append(re)
            cursor.close()
        except Exception as e:
            logging.error(e)
            if cursor != None:
                cursor.close()
        if echo:
            print(result)
        return result

    def find(self,sql,name=None,echo =True):
        cursor = None
        result = Model(table=None, data=None)
        try:
            if echo:
                print(sql)
            cursor = self.connection.cursor()
            reCount = cursor.execute(sql)
            col_names = [row[0] for row in cursor.description]
            if reCount:
                result = Model(data=zip(col_names, cursor.fetchone()), table=name)
            cursor.close()
        except Exception as e:
            logging.error(e)
            if cursor != None:
                cursor.close()
        if echo:
            print(result)
        return result

    def findOne(self,sql,echo=True):
        cursor = None
        result = 0
        try:
            if echo:
                print(sql)
            cursor = self.connection.cursor()
            reCount = cursor.execute(sql)
            if reCount:
                re = cursor.fetchone()
                result = re[0]
            cursor.close()
        except Exception as e:
            logging.error(e)
            if cursor != None:
                cursor.close()
        if echo:
            print(result)
        return result

    def execute(self,sql,echo=True):
        if echo:
            print(sql)
        cursor = None
        reCount = False
        sql = sql.strip()
        import re
        reg = re.compile(r"^(INSERT|REPLACE INTO)", re.IGNORECASE)
        isInsert = False if reg.search(sql) is None else True

        try:
            connection = self.connection
            cursor = connection.cursor()
            reCount = cursor.execute(sql)
            if isInsert:
                reCount = cursor.lastrowid
            connection.commit()
        except Exception as e:
            logging.error(e)
        finally:
            if cursor != None:
                cursor.close()
        return reCount



class SQLAlChemyConnection(ConnectionIntfer):

    def __init__(self,connection):
        super(SQLAlChemyConnection, self).__init__(connection)

    def select(self,sql,name=None,echo=True):
        from sqlalchemy import text
        cursor=None
        result = []
        try:
            if echo:
                print("sql: {}".format(sql))
            cursor = self.connection.execute(text(sql))
            if cursor:
                col_names = [row[0] for row in cursor.cursor.description]
                alls = cursor.fetchall()
                for v in alls:
                    re = Model(data=zip(col_names, v), table=name)
                    result.append(re)
                self.connection.commit()
        except Exception as e:
            print(e)
        finally:
            if cursor is not None:
                cursor.close()

        if echo:
            print("result: {}".format(result))
        return result



    def find(self, sql, name=None, echo=True):
        from sqlalchemy import text
        cursor = None
        result = Model(table=None, data=None)
        try:
            if echo:
                print("sql: {}".format(sql))

            cursor = self.connection.execute(text(sql))
            if cursor:
                col_names = [row[0] for row in cursor.cursor.description]
                result = Model(data=zip(col_names, cursor.fetchone()), table=name)
            self.connection.commit()
        except Exception as e:
            print(e)
        finally:
            if cursor != None:
                cursor.close()
        if echo:
            print("result: {}".format(result))
        return result


    def findOne(self, sql, echo=True):
        from sqlalchemy import text
        cursor = None
        result = 0
        try:
            if echo:
                print("sql: {}".format(text(sql)))
            cursor = self.connection.execute(sql)
            if cursor:
                re = cursor.fetchone()
                result = re[0]
        except Exception as e:
            print(e)
        finally:
            if cursor:
                cursor.close()
        if echo:
            print(result)
        return result

    def execute(self, sql, echo=True):
        from sqlalchemy import text
        if echo:
            print(sql)
        cursor = None
        reCount = False
        sql = sql.strip()
        import re
        reg = re.compile(r"^(INSERT|REPLACE INTO)", re.IGNORECASE)
        isInsert = False if reg.search(sql) is None else True

        try:
            cursor = self.connection.execute(text(sql))
            self.connection.commit()
            if isInsert:
                reCount = cursor.lastrowid
        except Exception as e:
            print(e)
        finally:
            if cursor != None:
                cursor.close()
        return reCount



class DB:
    """
    :return Query
    """
    @staticmethod
    def name(name:str) -> Query:
        return Query(name)

    @staticmethod
    def select(sql,name=None,echo = True) -> Model:
        return Configuration.getConnection().select(sql,name,echo)

    @staticmethod
    def find(sql,name=None,echo = True) -> Model:
        return Configuration.getConnection().find(sql, name, echo)

    @staticmethod
    def findOne(sql,echo = True):
        return Configuration.getConnection().findOne(sql, echo)

    @staticmethod
    def execute(sql:str,echo = True):
        return Configuration.getConnection().execute(sql, echo)

import types

class Configuration:
    # 前缀
    prefix=''
    # Builder
    builder=None
    # Connection
    connection=None

    # sqlalchemy
    sqlalchemy=None


    @staticmethod
    def getPrefix():
        return ''

    @staticmethod
    def init(prefix = '',builder=None,connection=None,SQLAlchemy=None):
        Configuration.prefix = prefix
        Configuration.connection = connection
        Configuration.builder = builder
        Configuration.sqlalchemy = SQLAlchemy

    @staticmethod
    def init_dict(options):
        if "prefix" in options:
            Configuration.prefix = options["prefix"]

        if "builder" in options:
            Configuration.builder = options["builder"]

        if "connection" in options:
            Configuration.connection = options["connection"]

        if "SQLAlchemy" in options:
            Configuration.sqlalchemy = options["SQLAlchemy"]


    """
    :return Builder
    """
    @staticmethod
    def getBuilder(query:Query):
        if Configuration.builder is None:
            raise NameError("Configuration.builder 未配置")
        return Configuration.builder(query)

    @staticmethod
    def getConnection() -> ConnectionIntfer:
        if Configuration.connection is None and Configuration.sqlalchemy is None:
            raise NameError("Configuration.connection 未配置")
        if Configuration.connection is not None:
            if type(Configuration.connection) == types.FunctionType:
                return RawConnection(Configuration.connection())
            return RawConnection(Configuration.connection)

        if Configuration.sqlalchemy is not None:
            connect = Configuration.sqlalchemy
            if type(connect) == types.FunctionType:
                return SQLAlChemyConnection(connect())

            return SQLAlChemyConnection(connect.session)


CACHE_DATABASE_FIELD = {}

class TableStruct:
    table=''
    pk=''
    columns=[]
    def __init__(self):
        self.pk = ''
        self.table = ''
        self.columns = []

    def addColumn(self,field='',type='',key='',PRI=False,default=None,null=False):
        self.columns.append(ColumnStruct(field,type,key,PRI,default,null))
        if PRI:
            self.pk = field
        return self


    def getColumns(self)->list:
        """
        :return:list[ColumnStruct]
        """
        return self.columns



class ColumnStruct:
    field=''
    key=''
    PRI=False
    default=None
    null=False
    type=''
    def __init__(self,field='',type='',key='',PRI=False,default=None,null=False):
        self.field = field
        self.key=key.lower()
        self.type=type.lower()
        self.PRI = PRI
        self.default = default
        self.null = null


import time

class Builder:
    query=None
    def __init__(self,query:Query):
        self.query = query

    @staticmethod
    def make(query:Query):
        return Builder(query)

    @property
    def selectSql(self):
        return "SELECT{DISTINCT} {FIELD} FROM {TABLE}{FORCE}{JOIN}{WHERE}{GROUP}{HAVING}{ORDER}{LIMIT} {LOCK}"

    @property
    def updateSql(self):
        return "UPDATE {TABLE} SET {SET}{JOIN}{WHERE} {LOCK}"

    @property
    def insertSql(self):
        return "{INSERT} INTO {TABLE} ({FIELD}) VALUES ({DATA})"

    @property
    def deleteSql(self):
        return "DELETE FROM {TABLE}{JOIN}{WHERE}{ORDER}{LIMIT} {LOCK}"


    def builderSelect(self):
        sql = self.selectSql
        return sql.format(
            DISTINCT=self.parseDistinct() ,
            FIELD=self.parseField() ,
            TABLE=self.parseTable() ,
            FORCE=self.parseForce() ,
            JOIN=self.parseJoin() ,
            WHERE=self.parseWhere() ,
            GROUP=self.parseGroup() ,
            HAVING=self.parseHaving(),
            ORDER=self.parseOrder(),
            LIMIT=self.parseLimit(),
            LOCK=self.parseLock(),
        )

    def getTableFind(self,table):
        return "SHOW COLUMNS FROM {}".format(table)


    def getDatabaseType(self,table)->TableStruct:
        if table in CACHE_DATABASE_FIELD:
            return CACHE_DATABASE_FIELD[table]

        result = TableStruct()
        try:
            sql = self.getTableFind(table)
            alls = Configuration.getConnection().select(sql,None,False)
            for re in alls:
                result.addColumn(
                    field=re['Field'],
                    type=re['Type'],
                    null=False if re['Null'] == 'NO' else True,
                    key=re['Key'],
                    default=re['Default'],
                    PRI=re['Key'] == 'PRI',
                )
        except Exception as e:
            print(e)

        CACHE_DATABASE_FIELD[table] = result
        return result


    def parseData(self,data,isInsert = False) -> dict:
        tableStruct = self.getDatabaseType(Configuration.prefix + self.query.name)
        result = {}

        for col in tableStruct.getColumns():
            """
            :type col ColumnStruct
            """
            # 更新的时候不理他
            if col.PRI and isInsert:
                continue
            field = col.field
            if field in data:
                content = data[field]
                if isinstance(content,list):
                    v0 = str(content[0]).lower()
                    v1 = content[1]
                    if v0 == 'inc':
                        result[field] = "{} + {}".format(field,v1)
                    elif v0 == 'dec':
                        result[field] = "{} - {}".format(field,v1)
                    else:
                        result[field] = v1
                else:
                    result[field] = self.formatString(content)
            else:
                if isInsert:
                    result[field] = self.formatString( self.getTypeDefault(col) )
        return result
        pass


    def getTypeDefault(self,col:ColumnStruct):
        type = col.type
        if type.find('int') != -1 or type.find('float') != -1 or type.find('double') != -1 or type.find('decimal') != -1:
            return '0'
        elif type.find("datatime") != -1 or type.find('timestamp') != -1:
            return time.strftime('%Y-%m-%d %H:%i:%s')
        elif type.find('date') != -1:
            return time.strftime('%Y-%m-%d')
        else:
            return ''



    def builderInsert(self,isReplace=False):
        sql = self.insertSql
        INSERT = "REPLACE" if isReplace else "INSERT"
        data = self.query.getData()

        formatData = self.parseData(data,True)

        keys = list(formatData.keys())
        values = list(formatData.values())

        #"{INSERT} INTO {TABLE} ({FIELD}) VALUES ({DATA})"
        return sql.format(
            INSERT=INSERT,
            TABLE=self.parseTable(),
            FIELD=",".join(keys),
            DATA=",".join(values)
        )

    def builderUpdate(self):
        sql = self.updateSql
        data = self.query.getData()

        formatData = self.parseData(data)
        sets = []
        for k,v in formatData.items():
            sets.append("{}={}".format(k,v))

        return sql.format(
            TABLE=self.parseTable(),
            SET=",".join(sets),
            JOIN=self.parseJoin(),
            WHERE=self.parseWhere(),
            LOCK=self.parseLock()
        )

    def builderDelete(self):
        sql = self.deleteSql
        #"DELETE FROM {TABLE}{JOIN}{WHERE}{ORDER}{LIMIT} {LOCK}"
        return sql.format(
            TABLE=self.parseTable(),
            JOIN=self.parseJoin(),
            WHERE=self.parseWhere(),
            ORDER=self.parseOrder(),
            LIMIT=self.parseLimit(),
            LOCK=self.parseLock()
        )

    def parseDistinct(self):
        if 'distinct' in self.query.options:
            return ' DISTINCT '
        return ''


    def parseField(self):
        if 'field' in self.query.options:
            field = self.query.options['field']
            return ",".join(field)
        return '*'

    def parseTable(self):
        name = Configuration.prefix + self.query.name
        if "alias" in self.query.options:
            name = name + " "+self.query.options['alias']

        return name

    def parseForce(self):
        if 'force' in self.query.options:
            field = self.query.options['force']
            return " FORCE INDEX ( {} ) ".format(field)
        return ''

    def parseJoin(self):
        if 'join' in self.query.options:
            joins = self.query.options['join']
            return " {} ".format(" ".join(joins))
        return ''

    def parseWhere(self):
        buffer = ""
        if 'where' in self.query.options:
            wheres = self.query.options['where']
            buffer = " WHERE "
            i=0
            for map in wheres:
                if i > 0:
                    buffer = buffer + (" {} ".format(map["connect"] if "connect" in map else "AND"))

                raw = map["raw"] if "raw" in map else False
                if raw:
                    buffer = buffer + (" {} ".format(map['name']))
                else:
                    key = map['name'] if "name" in map else ""
                    exp = map['exp'] if "exp" in map else "="
                    val = map['value'] if "value" in map else ""
                    buffer = buffer + " ( "
                    if key.find("|") != -1:
                        keys = key.split("|")
                        #buffer = buffer + " ( "
                        j=0
                        for k in keys:
                            if j>0:
                                buffer = buffer + " OR "

                            buffer = buffer + self.parseWhereItem(k,exp,val)
                            j=j+1
                    else:
                        buffer = buffer + self.parseWhereItem(key, exp, val)
                    buffer = buffer + " ) "

                i=i+1

        return buffer
        pass

    def parseWhereItem(self, key, exp, val):
        comparison = {
            'eq': '=', 'neq': '<>', 'gt': '>', 'egt': '>=', 'lt': '<', 'elt': '<=', 'notlike': 'NOT LIKE',
        }
        if exp in comparison:
            exp = comparison[exp]

        exp = exp.lower().strip()
        buffer = ""
        if exp == 'in' or exp == 'not in':
            inArrayList = self.getParseWhereValueArray(val)
            buffer = " {} {}( ".format(key,exp)
            i = 0
            for v in inArrayList:
                if i > 0:
                    buffer = buffer + ","
                buffer = buffer + self.formatString(v)
                i=i+1
            buffer = buffer + ")"

        elif exp == 'between' or exp == 'not between':
            buffer = " {} {} ".format(key, exp)
            inArrayList = self.getParseWhereValueArray(val)
            buffer = buffer + ("{} AND {}".format(self.formatString(inArrayList[0]),self.formatString(inArrayList[1])))
        else:
            if val is None:
                if exp == '=':
                    buffer = " {} is null ".format(key)
                elif exp == '!=':
                    buffer = " {} is not null ".format(key)
                else:
                    buffer = " {}{}'null' ".format(key,exp)
            else:

                buffer = " {} {} {} ".format(key,exp, self.formatString(val) )

        return buffer
        pass


    def getParseWhereValueArray(self,val):
        if isinstance(val,list):
            return val
        elif isinstance(val,str):
            return val.split(",")
        elif isinstance(val,dict):
            return list(val.values())
        elif isinstance(val,tuple):
            return val

        return [val]


    def formatString(self,value):
        val = str(value)
        return "'{}'".format(val.replace("'","\\'"))

    def parseGroup(self):
        if "group" in self.query.options:
            group = self.query.options['group']
            return "GROUP BY {}".format(",".join(group))
        return ""

    def parseHaving(self):
        if "having" in self.query.options:
            having = self.query.options['having']

            return " having {} ".format(having)
        return ''

    def parseOrder(self):
        if "order" in self.query.options:
            order = self.query.options['order']
            return " ORDER BY {} ".format(",".join(order))
        return ''

    def parseLimit(self):
        if 'limit' in self.query.options:
            limit = self.query.options['limit']
            offset = limit['offset']
            size = limit['size']

            if not offset:
                return " LIMIT {} ".format(size)

            return " LIMIT {},{} ".format(offset,size)
        return ''
        pass

    def parseLock(self):
        if "lock" in self.query.options:
            return self.query.options['lock']
        return ''



class MysqlBuilder(Builder):
    def __init__(self,query:Query):
        super(MysqlBuilder, self).__init__(query)
