from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from .models import Qiandaoxinxi
from core import utils,DB



# Create your views here.

from core import Blueprint

# 创建访问路由对象
router=Blueprint("qiandaoxinxi")


# 设置页面搜素表单填写的数据，设置搜素条件
def getWhere(request,qs):

    if request.GET.get("qiandaobianhao"):
        qs = qs.filter(qiandaobianhao__contains=request.GET.get("qiandaobianhao"))
    if request.GET.get("qiandaomingcheng"):
        qs = qs.filter(qiandaomingcheng__contains=request.GET.get("qiandaomingcheng"))



    # 获取排序字段
    orderby = utils.param( "orderby", "id")
    # 设置排序
    sort = utils.param( "sort", "DESC").upper()
    if sort == "DESC":
        qs = qs.order_by("-" + orderby)
    else:
        qs = qs.order_by(orderby)

    return qs


# 管理员列表页面

@router.route('admin/list/')
def adminlist(request):

    if not utils.checkLogin():
        return utils.showError("请登录后操作","/login/");

    qs = getWhere(request,Qiandaoxinxi.objects)

    if utils.session("cx") == "学生":
        qs = qs.filter(qiandaobanji=utils.session("suozaibanji"))

    qs = qs.all()

    # 分页数
    pagesize = utils.param( "pagesize", 12)
    # 分页获取数据
    paginator = Paginator(qs, pagesize)
    # 获取当前page页码，默认为1
    page = request.GET.get('page', 1)
    try:
        lists = paginator.page(page)  # 分页
    except PageNotAnInteger:
        lists = paginator.page(1)
    except EmptyPage:
        lists = paginator.page(paginator.num_pages)

    # 判断是否有分页
    is_paginated = True if paginator.num_pages > 1 else False
    # 获取页码
    page_range = paginator.get_elided_page_range(page, on_each_side=3, on_ends=2)
    # 获取排序字段,默认发布时间
    orderby = utils.param( "orderby", "id")
    # 是升序还是降序，默认降序
    sort = utils.param( "sort", "desc")
    # 配置分页信息
    page = utils.formatPage(paginator.count,pagesize)



    # 渲染模板文件：templates/qiandaoxinxi/list.html
    return render(request , "qiandaoxinxi/list.html" , locals() )


# 发布人列表页面
@router.route('admin/faburen/')
def faburen(request):
    # 设置查询条件
    qs = getWhere(request,Qiandaoxinxi.objects)
    # 过滤为发布人用户的内容
    qs = qs.filter(faburen=request.session['username'])

    qs = qs.all()
    # 分页数
    pagesize = utils.param( "pagesize", 12)
    # 分页获取数据
    paginator = Paginator(qs, pagesize)
    # 获取当前page页码，默认为1
    page = request.GET.get('page', 1)
    try:
        lists = paginator.page(page)  # 分页
    except PageNotAnInteger:
        lists = paginator.page(1)
    except EmptyPage:
        lists = paginator.page(paginator.num_pages)

    # 判断是否有分页
    is_paginated = True if paginator.num_pages > 1 else False
    # 获取页码
    page_range = paginator.get_elided_page_range(page, on_each_side=3, on_ends=2)
    # 配置分页信息
    page = utils.formatPage(paginator.count,pagesize)

    # 获取排序字段,默认发布时间
    orderby = utils.param( "orderby", "id")
    # 是升序还是降序，默认降序
    sort = utils.param( "sort", "desc")



    # 渲染模板文件：templates/qiandaoxinxi/faburen.html
    return render(request , "qiandaoxinxi/faburen.html" , locals() , )




#后台添加页面
@router.route('admin/add/')
def adminadd(request):
    # 判断是否登录
    if not utils.checkLogin():
        return utils.showError("请登录后操作","/login/");




    # 渲染模板文件：templates/qiandaoxinxi/add.html
    return render(request , "qiandaoxinxi/add.html",locals())




# 编辑页面
@router.route('admin/updt/')
def adminupdt(request):
    # 获取提交上来id 值
    id = request.GET.get("id")
    # 根据id 获取一行数据
    mmm = Qiandaoxinxi.objects.get(pk = id)
    # 数据为 None 则提示没有相关数据
    if mmm is None:
        return utils.showError("没有找到相关数据")





    # 渲染模板文件：templates/qiandaoxinxi/updt.html
    return render(request, "qiandaoxinxi/updt.html" , locals())




# 后台详情页面
@router.route('admin/detail/')
def admindetail(request):
    # 获取参数id
    id = request.GET.get("id")
    # 根据参数id 获取一行数据
    map = Qiandaoxinxi.objects.get(pk=id)

    # 渲染模板文件：templates/qiandaoxinxi/detail.html
    return render(request , "qiandaoxinxi/detail.html" , locals())


# 删除数据
@router.route('delete/')
def delete(request):
    # 获取id 值
    ids = request.GET.getlist("id")

    for id in ids:
        # 根据id 获取一行数据
        map = Qiandaoxinxi.objects.get(pk = id)

        # 删除数据
        map.delete()

    return utils.showSuccess("删除成功")




# 插入签到信息模块一行数据
@router.route('insert/')
def insert(request):

    # 将post 数据进行copy一份
    post = request.POST.copy()
    data = {
        'qiandaobianhao': utils.param('qiandaobianhao',''),
        'qiandaobanji': utils.param('qiandaobanji',utils.param('qiandaobanji',None)),
        'qiandaomingcheng': utils.param('qiandaomingcheng',''),
        'qiandaoshijian': utils.param('qiandaoshijian',''),
        'jiezhishijian': utils.param('jiezhishijian',''),
        'shuoming': utils.param('shuoming',''),
        'faburen': utils.param('faburen',''),

    }
    if data['faburen'] == '':
        data['faburen'] = utils.session( "username")



    # 新建Qiandaoxinxi 对象，用QiandaoxinxiModel 对象进行对数据进行插入
    model = Qiandaoxinxi(**data)
    # 执行插入数据
    model.save(force_insert = True)

    # 获取有没有设置返回页面地址,有则使用，没有则使用上一页的地址
    referer = utils.param("referer" , request.headers.get('referer'))
    return utils.showSuccess( "添加成功" , referer)

# 根据id 更新一行数据
@router.route('update/')
def update(request):
    # 获取提交的id值
    charuid = request.POST.get('id')
    # 拷贝一份数据
    post = request.POST.copy()
    old = Qiandaoxinxi.objects.get(pk = charuid)
    data = {
        'id': charuid,
        'qiandaobianhao': utils.param('qiandaobianhao',old.qiandaobianhao),
        'qiandaobanji': utils.param('qiandaobanji',utils.param('qiandaobanji',old.qiandaobanji)),
        'qiandaomingcheng': utils.param('qiandaomingcheng',old.qiandaomingcheng),
        'qiandaoshijian': utils.param('qiandaoshijian',old.qiandaoshijian),
        'jiezhishijian': utils.param('jiezhishijian',old.jiezhishijian),
        'shuoming': utils.param('shuoming',old.shuoming),
        'faburen': utils.param('faburen',old.faburen),

    }


    # 新建Qiandaoxinxi 对象，用QiandaoxinxiModel 对象进行对数据进行更新
    model = Qiandaoxinxi(**data)
    # 执行更新操作
    model.save(force_update = True)

    # 获取有没有设置返回页面地址,有则使用，没有则使用上一页的地址
    referer = utils.param( "referer" , request.headers.get('referer'))


    return utils.showSuccess( "修改成功" , referer)



