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

# 部门管理


# 用户管理
def user_list(request):
    """获取用户列表"""
    from app.utils.pagination import Pagination
    user_list = UserInfo.objects.all()

    user_queryset = Pagination(request, queryset=user_list)
    context = {
        "list_queryset": user_queryset.page_queryset,
        "page_string": user_queryset.html(),  # 页码
    }
    # for u in user_list:
    #     print(
    #         u.id,
    #         u.name,
    #         u.password,
    #         u.age,
    #         u.create_time.strftime("%Y-%m-%d-%H-%M"),
    #         u.depart.title,
    #         u.get_gender_display(),
    #         u.zone
    #     )
    return render(request, 'user_list.html', context)
def user_add(request):
    """添加用户"""
    # 将参数作为字典放到前端获取的位置
    context = {'gender_choices': UserInfo.gender_choices,
               'depart_list': Department.objects.all()
               }
    if request.method == "GET":
        return render(request, "user_add.html", context)
    name = request.POST.get("name")
    password = request.POST.get("pwd")
    account = request.POST.get("ac")
    age = request.POST.get("age")
    create_time = request.POST.get("ctime")
    zone = request.POST.get("zone")
    depart_id = request.POST.get("depart")
    gender_id = request.POST.get("gender")
    print(depart_id, name)

    # 添加到数据库中
    UserInfo.objects.create(name=name, password=password, account=account, age=age, create_time=create_time, zone=zone
                            , depart_id=depart_id, gender=gender_id)
    return redirect("/user/list/")
# 下面这个方法中的form来自上面这个类
def user_model_list_add(request):
    """ 添加用户 （ModelForm版本） """
    if request.method == "GET":
        form = UserModelForm()  # 实例化字段
        return render(request, 'user_modeladd.html', {"form": form})
    # 用户POST提交数据，数据校验
    form_data = UserModelForm(data=request.POST)
    if form_data.is_valid():
        # 如果数据合法 保存到数据库
        # {'name': '王志伟444', 'password': '41234', 'account': Decimal('123125'), 'age': 3, 'create_time': datetime.datetime(2022, 2, 8, 0, 0, tzinfo=backports.zoneinfo.ZoneI
        # nfo(key='UTC')), 'zone': '北京', 'depart': <Department: HR部门>, 'gender': 2}
        print(form_data.cleaned_data)
        form_data.save()
        return redirect('/user/list')
    return render(request, 'user_modeladd.html', {"form": form_data})

def user_model_edit(request, nid):
    """ 编辑用户 """

    # 由于读取GET和编辑保存POST时都需要知道是哪一条数据，故而可以把获取的数据统一放到这里来
    row_object = UserInfo.objects.filter(id=nid).first()

    if request.method == "GET":
        # 根据ID去数据库获取要编辑的那一行数据（对象）
        # row_object = UserInfo.objects.filter(id=nid).first()
        form = UserModelForm(instance=row_object)
        return render(request, 'user_edit.html', {"form": form})

    # 编辑数据时，填写后的内容要保存到哪一条数据需要，所以还需要写下面这一行
    # row_object = UserInfo.objects.filter(id=nid).first()
    form = UserModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        # save是默认保存的是用户输入的所有数据，如果想要在用户输入以外的字段增加值：
        # form.instance.字段 = 值
        form.instance.age = 15
        form.save()
        return redirect('/user/list')
    return render(request, 'user_edit.html', {"form": form})
def user_delete(request, nid):
    """  删除用户  """
    UserInfo.objects.filter(id=nid).delete()
    return redirect('/user/list')


#  靓号管理






