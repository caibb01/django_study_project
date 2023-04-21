# 导入django的shortcuts使用函数返回的参数,到达html或者是直接返回或重定向
from django.shortcuts import render, HttpResponse, redirect
# 导入要使用到的数据库模块
from app.models import *
# 使用到这里面时可以抛出异常
from django.core.exceptions import ValidationError
# 使用到这个core中的validators里面的添加验证器
from django.core import validators
# 使用到分页时,需要向上取整
import math
# 由于靓号列表中返回的内容,但是前端页面显示的是代码,与逾期不一样,是字符串而不是编译为html,需要标记为安全的
from django.utils.safestring import mark_safe
from django import forms
from app.utils.modelform import UserModelForm,PrettyNumForm,PrettyEditNumForm,UserModelForm



def prettynum_list(request):
    """ 靓号列表 """
    """ 手机号的搜索功能 """
    # 获取页面传来的get的num内容,通过内容进行搜索,并返回给页面
    search_num = request.GET.get("num", '')
    # 将查询的条件字典化
    search_dict = {"mobile__contains": search_num}

    """ 手机号的分页功能 """
    # 获取查询返回的page是第几页
    from app.utils.pagination import Pagination
    queryset = PrettyNum.objects.filter(**search_dict).order_by("-level")

    page_object = Pagination(request, queryset, )
    context = {
        "search_num": search_num,
        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_str_list": page_object.html(),  # 页码
    }
    return render(request, 'prettynum_list.html', context)

def prettynum_add(request):
    if request.method == 'GET':
        form = PrettyNumForm()
        return render(request, 'prettynum_add.html', {"form": form})
    # 接收页面返回的内容
    prettynum_add_data = PrettyNumForm(data=request.POST)
    # 判断是否合法,合法就保存到数据库并重定向到主页
    if prettynum_add_data.is_valid():
        prettynum_add_data.save()
        return redirect("/prettynum/list")
    return render(request, 'prettynum_add.html', {"form": prettynum_add_data})


def prettynum_edit(request, nid):
    # 展示编辑页面的数据为所点击的数据
    row_object = PrettyNum.objects.filter(id=nid).first()
    if request.method == "GET":
        form = PrettyEditNumForm(instance=row_object)
        return render(request, 'prettynum_edit.html', {"form": form})
    form = PrettyEditNumForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.instance.zone = "北京"  # 设置修改后指定字段的默认值
        form.save()
        return redirect("/prettynum/list")
    return render(request, 'prettynum_edit.html', {"form": form})

def prettynum_delete(request, nid):
    PrettyNum.objects.filter(id=nid).delete()
    return redirect("/prettynum/list")
    # return render(request, 'prettynum_edit.html', {"form": form})
