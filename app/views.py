from django.shortcuts import render, HttpResponse, redirect
from app.models import *


# 部门管理
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


# 用户管理
def user_list(request):
    """获取用户列表"""
    user_list = UserInfo.objects.all()
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
    return render(request, 'user_list.html', {"user_list": user_list})


def user_add(request):
    """添加用户"""
    # 将参数作为字典放到前端获取的位置
    context = {'gender_choices': UserInfo.gender_choices,
               'depart_list': Department.objects.all()
               }
    if request.method == "GET":
        return render(request, "user_add.html",context)
    name = request.POST.get("name")
    password = request.POST.get("pwd")
    account = request.POST.get("ac")
    age = request.POST.get("age")
    create_time = request.POST.get("ctime")
    zone = request.POST.get("zone")
    depart_id = request.POST.get("depart")
    gender_id = request.POST.get("gender")
    print(depart_id,name)


    # 添加到数据库中
    UserInfo.objects.create(name=name, password=password, account=account, age=age, create_time=create_time, zone=zone
                            , depart_id=depart_id, gender=gender_id)
    return redirect("/user/list/")


#  ################################  ModelForm  ################################
# 使用到ModelForm就要用到django的一个类forms，所以要导入
from django import forms

class UserModelForm(forms.ModelForm):
    class Meta:
        model = UserInfo  # 注意这里是用model而不是models，因为我们只是用到几个，而不是这张表的全部字段
        fields = ["name", "password", "account", "age", "create_time", "zone", "depart", "gender"]
        """ 下面这么写给每一个都加上样式也可以，但是这么做会比较麻烦 """
        """ fields这里面的内容是【一个字段名+字段对应的对象，典型的例子部门depart】
        {'name': <django.forms.fields.CharField object at 0x000002979134F4F0> 
         'password': <django.forms.fields.CharField object at 0x000002979134F400>
         'account': <django.forms.fields.DecimalField object at 0x000002979134F5B0>
         'age': <django.forms.fields.IntegerField object at 0x000002979134F3D0>, ......
        """
        # widgets = {
        #     "name": forms.TextInput(attrs={"class": "form-control"}),
        #     "password": forms.PasswordInput(attrs={"class": "form-control"}),
        #     "age": forms.TextInput(attrs={"class": "form-control"}),
        # }
        """ 使用下面这种方法，比较开发 """
    # 重新定义__init__的方法
    def __init__(self, *args, **kwargs):
        # 继承父类__init__的方法
        super().__init__(*args, **kwargs)

        # 循环找到所有的插件，添加"class": "form-control",
        for name, field in self.fields.items():
            # if name == "age":
            #     continue # 这里可以设置指定字段的样式
            # print(name, field)  # 查看返回的内容是什么
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}


# 下面这个方法中的form来自上面这个类
def user_model_list_add(request):
    """ 添加用户 （ModelForm版本） """
    form = UserModelForm()   # 实例化字段
    return render(request, 'user_modeladd.html', {"form": form})
