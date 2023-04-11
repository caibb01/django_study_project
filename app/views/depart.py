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

def depart_list(request):
    """获取部门列表数据"""
    if request.method == "GET":
        # 获取数据库的部门列表数据，返回一行一行，每一行是一个对象
        depart_list = Department.objects.all()
    return render(request, 'depart_list.html', {"depart_list": depart_list})


def depart_add(request):
    """添加部门"""
    if request.method == "GET":
        return render(request, 'depart_add.html')

    # 获取用户POST提交过来的数据
    title = request.POST.get("title")

    # 将用户提交的数据保存到数据库
    Department.objects.create(title=title)

    # 重定向到部门列表
    return redirect("/depart/list/")


def depart_delete(request):
    """删除部门"""

    # 获取ID http://127.0.0.1:8000/depart/delete/?id=?
    mid = request.GET.get("id")

    # 到数据库删除对应的数据
    Department.objects.filter(id=mid).delete()

    # 重定向到部门列表
    return redirect("/depart/list/")


# http://127.0.0.1:8000/depart/8/edit/
# http://127.0.0.1:8000/depart/2/edit/
# http://127.0.0.1:8000/depart/5/edit/
# 上面这个就是html中的/depart/{{ obj.id }}/edit，然后和urls中的正则<int:edit_id>
def depart_edit(request, edit_id):
    """修改部门"""
    if request.method == "GET":
        # 根据edit_id 获取数据的[obj.id]
        row_object = Department.objects.filter(id=edit_id).first()
        return render(request, 'depart_edit.html', {"titles": row_object})

    # 获取用户提交的标题
    edit_title = request.POST.get("edit_title")

    # 根据ID找到数据库中的数据并进行更新
    Department.objects.filter(id=edit_id).update(title=edit_title)

    # 重定向会部门列表
    return redirect("/depart/list/")

