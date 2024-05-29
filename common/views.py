from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from core import request,utils,DB

# Create your views here.
from core import Blueprint
import json



router = Blueprint("commons")



@router.route("")
def index(request:HttpRequest):

    return render(request,"index.html",locals())



# 系统登录
@router.route("/login/")
def login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        cx       = request.POST.get('cx')

        if "a" in request.GET:
            pagerandom = request.POST.get('pagerandom')
            captcha = request.session["captchaCode"]
            if not pagerandom:
                return utils.showError( "请填写验证码")
            if pagerandom != captcha:
                return utils.showError( "验证码错误")

        if not username:
            return utils.showError( "请填写账号")
        if not password:
            return utils.showError( "请填写密码")
        if not cx:
            return utils.showError( "请选择相应角色")
        qs = None
        issh = False
        if cx == '管理员':
            from admins.models import Admins
            
            qs = Admins.objects.filter(username=username , pwd=password)
        if cx == '教师':
            from jiaoshi.models import Jiaoshi
            
            qs = Jiaoshi.objects.filter(gonghao=username , mima=password)
        if cx == '学生':
            from xuesheng.models import Xuesheng
            
            qs = Xuesheng.objects.filter(xuehao=username , mima=password)


        if qs is None:
            return utils.showError('没有找到相关角色')

        list = qs.values()

        if not list:
            return utils.showError("账号或密码错误")

        user = list[0]
        if issh and user['issh'] != '是':
            return utils.showError('账号审核中')

        request.session['cx'] = cx
        request.session['login'] = cx
        request.session['username'] = username

        for key,value in user.items():
            request.session[key] = str(value)

        if 'referer' in request.POST:
            referer = request.POST.get('referer')
        else:
            referer = '/main'

        return utils.showSuccess("登录成功" , referer)
    else:
        # 访问页面
        return render(request,'login.html' , locals())




@router.route('sh/')
def sh(request):
    tablename = utils.input( "tablename" , "")
    yuan = utils.input( "yuan" , "")
    id = int(utils.input( "id" , 0))

    if yuan == "否" or yuan == "":
        sql = "UPDATE %s SET issh='是' WHERE id='%s' " %(tablename,id,)
    else:
        sql = "UPDATE %s SET issh='否' WHERE id='%s' " %(tablename,id,)

    DB.execute(sql)

    return utils.showSuccess( "审核成功" if yuan == '否' or not yuan else '已取消审核')









# 生成验证码
# https://www.cnblogs.com/3one/p/8461306.html  参考这个网站做得一个函数
@router.route("captch/")
def captcha(request):
    from .captch import create_validate_code
    img , strs=create_validate_code(size=(120 , 30))
    request.session["captchaCode"] = strs
    from io import BytesIO
    f = BytesIO()
    img.save(f, "png")
    data = f.getvalue()
    print("验证码值：%s" % (strs,))

    return HttpResponse(data, content_type='image/png')


@router.route("main/")
def main(request):
    if not utils.checkLogin():
        return utils.showError("请登录后操作", "/login/")
    return render(request,"main.html",locals())

@router.route("logout/")
def logout(request):
    request.session.clear()
    request.session.flush()
    return redirect('/')

@router.route("top/")
def top(request):
    return render(request , 'top.html')

@router.route("mygo/")
def mygo(request):
    return render(request , 'mygo.html')



@router.route("/mod/")
def mod(request):
    if not utils.checkLogin():
        return utils.showError("请登录后操作", "/login/")
		
    if request.method == 'POST':
        oldPwd = request.POST.get("oldPwd" , "")
        newPwd = request.POST.get("newPwd" , "")
        newPwd2 = request.POST.get("newPwd2" , "")

        if not all([oldPwd,newPwd2,newPwd]):
            return utils.showError("请填写原密码或新密码或确认密码")

        if newPwd != newPwd2:
            return utils.showError( "两次输入密码错误")
        cx  = request.session["login"]
        username = request.session["username"]
        qs = None
        mimafield = ''

        if cx == '管理员':
            from admins.models import Admins
                        
            qs = Admins.objects.filter(username=username , pwd=oldPwd)
            mimafield = 'pwd'
        if cx == '教师':
            from jiaoshi.models import Jiaoshi
                        
            qs = Jiaoshi.objects.filter(gonghao=username , mima=oldPwd)
            mimafield = 'mima'
        if cx == '学生':
            from xuesheng.models import Xuesheng
                        
            qs = Xuesheng.objects.filter(xuehao=username , mima=oldPwd)
            mimafield = 'mima'


        if qs is None:
            return utils.showError( "没有该用户")

        values = qs.all()
        if not len(values):
            return utils.showError( "原密码错误")

        user = values[0]
        setattr(user , mimafield , newPwd)
        user.save()
        return utils.showSuccess("密码修改成功" , "/mod/")
    else:
        return render( request , 'mod.html',locals() )




@router.route("/sy/")
def sy(request):
    if not utils.checkLogin():
        return utils.showError("请登录后操作", "/login/")



    return render(request,"sy.html",locals())







@router.route('/checkon')
def checkon(request):
    table = utils.input('table')
    col = utils.input('col')
    checktype = utils.input('checktype')
    val = utils.input(col)
    qs = DB.name(table).where(col,val)
    if checktype == 'update':
        id = utils.input('id')
        qs.where('id' , 'neq',id)

    count = qs.count()
    if count:
        return HttpResponse('false')
    else:
        return HttpResponse('true')


@router.route('/selectUpdateSearch/')
def selectUpdateSearch(request):
    where = json.loads(request.POST.get('where'))
    table = request.POST.get('table')

    qs = DB.name(table)
    pagesize = 50

    for key,value in where.items():
        if key == 'limit':
            pagesize = int(value)
        else:
            if isinstance(value , str) or isinstance(value , int):
                qs.where(key,value)
            else:
                exp = value[0]
                val = value[1]
                qs.where(key, exp,val)

    qs.limit(pagesize)
    qs.order("id asc")
    lists = qs.select()

    print(lists)
    return HttpResponse(json.dumps(lists,cls=utils.DecimalEncoder),content_type='applocation/json')


@router.route('/qiandaotongji')
def query(request:HttpRequest):

    where = "1=1"

    if utils.input('xuehao'):
        where += " AND xuehao LIKE '%{}%' ".format(utils.input('xuehao'))

    if utils.input('suozaibanji'):
        where += " AND suozaibanji='{}' ".format(utils.input('suozaibanji'))

    if "教师" == utils.session('cx'):
        where += " AND suozaibanji='{}' ".format(utils.session('suodaibanji'))

    if "学生" == utils.session('cx'):
        where += " AND id='{}' ".format(utils.session('id'))

    lists = DB.name('xuesheng').where(where).select()
    for v in lists:
        daiqiandaoshu = DB.name("qiandaoxinxi").where("qiandaobanji",v['suozaibanji']).count()
        qiandaoshu = DB.name('xueshengqiandao').where('qiandaobanji',v['suozaibanji']).where('xueshengxuehao',v['xuehao']).count()
        chidaoshu = DB.name('xueshengqiandao').where('qiandaobanji',v['suozaibanji']).where('shifouchidao','迟到').where('xueshengxuehao',v['xuehao']).count()
        kuangke = daiqiandaoshu - qiandaoshu

        if daiqiandaoshu > 0:
            qiandaolv = "%.2f"%(qiandaoshu / daiqiandaoshu * 100,)
        else:
            qiandaolv = 0

        v['daiqiandaoshu'] = daiqiandaoshu
        v['qiandaoshu'] = qiandaoshu
        v['chidaoshu'] = chidaoshu
        v['kuangke'] = kuangke
        v['qiandaolv'] = qiandaolv


    return render(request,"qiandaolv.html",locals())


@router.route('/query')
def query(request:HttpRequest):
    map = json.loads(request.body)
    if not isinstance(map,dict):
        return utils.showError("数据错误")
    if "name" not in map:
        return utils.showError("找不到名称")
    if "options" not in map and not isinstance(map['options'],dict):
        return utils.showError("找不到属性")
    if "func" not in map:
        return utils.showError("找不到引用")

    options = map['options']
    qs = DB.name(map['name'])
    qs.options = options
    func = map['func']
    args = map.get("args")
    attrs = getattr(qs,func)
    if attrs:
        if args and len(args):
            res = attrs(*args)
        else:
            res = attrs()
        data = json.dumps({
            'code':0,
            'data':res
        })
    else:
        data = json.dumps({
            'code': 1,
            'msg': '找不到方法',
            'data': None
        })
    return HttpResponse(data, content_type='applocation/json')

@router.route('/tableAjax')
def tableAjax(request):
    table = utils.input('table')
    id = utils.input('id')
    return HttpResponse(json.dumps(DB.name(table).find(id)))
    pass

import os,hashlib
def get_file_md5(file):
    f_md5 = hashlib.md5(file.read())
    return f_md5.hexdigest()

def save_upload_file(PostFile, FilePath):
    try:
        f = open(FilePath, 'wb')
        for chunk in PostFile.chunks():
            f.write(chunk)
    except Exception as E:
        f.close()
        return u"写入文件错误: {}".format(E.message)
    f.close()
    return u"SUCCESS"

@router.route('/upload/')
def upload(request:HttpRequest):
    file = request.FILES.get('upfile')

    state = "SUCCESS"
    if file is None:
        return HttpResponse(json.dumps({'state':'ERROR'}), content_type="application/json")

    BASE_DIR = os.path.abspath('static')
    BASE_DIR = BASE_DIR + "/upload/"
    if not os.path.exists(BASE_DIR):
        os.makedirs(BASE_DIR)

    size = file.size
    name, ext = os.path.splitext(file.name)

    stream = file.file
    md5 = get_file_md5(stream)
    stream.seek(0)
    if state == 'SUCCESS':
        state = save_upload_file(file,BASE_DIR+md5+ext)

    return_info = {
        # 保存后的文件名称
        'url': '/static/upload/'+md5+ext,
        'original': name,  # 原始文件名
        'type': ext,
        'state': state,  # 上传状态，成功时返回SUCCESS,其他任何值将原样返回至图片上传框中
        'size': size
    }
    return HttpResponse(json.dumps(return_info),content_type='application/json')
