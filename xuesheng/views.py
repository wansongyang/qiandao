from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from .models import Xuesheng
from core import utils,DB



# Create your views here.

from core import Blueprint

# 创建访问路由对象
router=Blueprint("xuesheng")


# 设置页面搜素表单填写的数据，设置搜素条件
def getWhere(request,qs):

    if request.GET.get("xuehao"):
        qs = qs.filter(xuehao__contains=request.GET.get("xuehao"))
    if request.GET.get("suozaibanji"):
        qs = qs.filter(suozaibanji=request.GET.get("suozaibanji"))



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

    qs = getWhere(request,Xuesheng.objects)
    if utils.session("cx") == "教师":
        qs = qs.filter(suozaibanji=utils.session("suodaibanji"))
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



    # 渲染模板文件：templates/xuesheng/list.html
    return render(request , "xuesheng/list.html" , locals() )






#后台添加页面
@router.route('admin/add/')
def adminadd(request):
    # 判断是否登录
    if not utils.checkLogin():
        return utils.showError("请登录后操作","/login/");




    # 渲染模板文件：templates/xuesheng/add.html
    return render(request , "xuesheng/add.html",locals())




# 编辑页面
@router.route('admin/updt/')
def adminupdt(request):
    # 获取提交上来id 值
    id = request.GET.get("id")
    # 根据id 获取一行数据
    mmm = Xuesheng.objects.get(pk = id)
    # 数据为 None 则提示没有相关数据
    if mmm is None:
        return utils.showError("没有找到相关数据")




    # 设置为编辑资料
    updtself=0

    # 渲染模板文件：templates/xuesheng/updt.html
    return render(request, "xuesheng/updt.html" , locals())


# 更新个人资料
@router.route('admin/updtself/')
def adminupdtself(request):
    # 获取session 中的id值，
    id = request.session['id']
    # 根据id 获取一行数据
    mmm = Xuesheng.objects.get(pk = id)
    # 数据为 None 则提示没有相关数据
    if mmm is None:
        return utils.showError("没有找到相关数据")

    # 设置为更新用户资料
    updtself = 1
    # 渲染模板文件：templates/xuesheng/updtself.html
    return render(request, "xuesheng/updtself.html" , locals())


# 后台详情页面
@router.route('admin/detail/')
def admindetail(request):
    # 获取参数id
    id = request.GET.get("id")
    # 根据参数id 获取一行数据
    map = Xuesheng.objects.get(pk=id)

    # 渲染模板文件：templates/xuesheng/detail.html
    return render(request , "xuesheng/detail.html" , locals())


# 删除数据
@router.route('delete/')
def delete(request):
    # 获取id 值
    ids = request.GET.getlist("id")

    for id in ids:
        # 根据id 获取一行数据
        map = Xuesheng.objects.get(pk = id)

        # 删除数据
        map.delete()

    return utils.showSuccess("删除成功")




# 插入学生模块一行数据
@router.route('insert/')
def insert(request):

    # 将post 数据进行copy一份
    post = request.POST.copy()
    data = {
        'xuehao': utils.param('xuehao',''),
        'mima': utils.param('mima',''),
        'xingming': utils.param('xingming',''),
        'xingbie': utils.param('xingbie',''),
        'lianxidianhua': utils.param('lianxidianhua',''),
        'suozaibanji': utils.param('suozaibanji',utils.param('suozaibanji',None)),
        'jianjie': utils.param('jianjie',''),

    }



    # 新建Xuesheng 对象，用XueshengModel 对象进行对数据进行插入
    model = Xuesheng(**data)
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
    old = Xuesheng.objects.get(pk = charuid)
    data = {
        'id': charuid,
        'xuehao': utils.param('xuehao',old.xuehao),
        'mima': utils.param('mima',old.mima),
        'xingming': utils.param('xingming',old.xingming),
        'xingbie': utils.param('xingbie',old.xingbie),
        'lianxidianhua': utils.param('lianxidianhua',old.lianxidianhua),
        'suozaibanji': utils.param('suozaibanji',utils.param('suozaibanji',old.suozaibanji)),
        'jianjie': utils.param('jianjie',old.jianjie),

    }


    # 新建Xuesheng 对象，用XueshengModel 对象进行对数据进行更新
    model = Xuesheng(**data)
    # 执行更新操作
    model.save(force_update = True)

    updtself = request.POST.get("updtself","0")
    if updtself == '' or updtself == '0':
        # 获取有没有设置返回页面地址,有则使用，没有则使用上一页的地址
        referer = utils.param( "referer" , request.headers.get('referer'))
    else:
        referer = "/xuesheng/admin/updtself/"


    return utils.showSuccess( "修改成功" , referer)



