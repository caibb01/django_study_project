from django.shortcuts import render, redirect, HttpResponse

from app.utils.pagination import Pagination
from app.models import Admin
from app.utils.encrypt import md5


def admin_list(request):
    # 检查用户是否以登录，以登录，继续想走下去，未登录，跳转回登陆页面
    # 用户发送请求，获取cookie随机字符串，拿着随机字符串看看session中有没有
    info = request.session.get("info")

    """ 获取管理员 """
    search_detail = request.GET.get("num", '')
    # 将查询的条件字典化
    search_dict = {"username__contains": search_detail}

    """ 手机号的分页功能 """
    # 获取查询返回的page是第几页
    admin_queryset = Admin.objects.filter(**search_dict).order_by("id")

    page_object = Pagination(request, queryset=admin_queryset)

    context = {
        "search_detail": search_detail,
        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_str_list": page_object.html(),  # 页码
        "page_str_list": page_object.html(),  # 页码
    }

    return render(request, 'admin_list.html', context)


from django import forms
from django.core.exceptions import ValidationError
from app.utils.bootstrap import BootStrapModelForm


class AdminAddModelForms(BootStrapModelForm):
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput
    )

    class Meta:
        model = Admin
        fields = '__all__'
        widgets = {
            "password": forms.PasswordInput(render_value=True)  # 这里表示密码不一致后不清空
        }

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)

    def clean_confirm_password(self):
        password = self.cleaned_data.get("password")
        confirm_password = md5(self.cleaned_data.get("confirm_password"))
        if password != confirm_password:
            raise ValidationError("密码不一致")
        return password


def admin_add(request):
    """   添加管理员  """
    title = "新增管理员"
    if request.method == "GET":
        form = AdminAddModelForms
        return render(request, "change.html", {"form": form, "title": title})
    form = AdminAddModelForms(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/admin/list/")
    return render(request, "change.html", {"form": form, "title": title})


class AdminEditModelForms(BootStrapModelForm):
    class Meta:
        model = Admin
        fields = ['username']

    def clean_username(self):
        input_username = self.cleaned_data.get("username")
        #     当前编辑的是哪一行ID:self.instance.pk  pk是主键,exclude就是除了这条id数据外，是否还有存在这个名字的，如果存在就返回True
        exists = Admin.objects.exclude(id=self.instance.pk).filter(username=input_username).exists()
        print(exists)
        if exists:
            raise ValidationError("该管理员用户名已存在")
        return input_username


def admin_edit(request, nid):
    title = "编辑管理员"
    one_objects = Admin.objects.filter(id=nid).first()
    if not one_objects:  # 判断数据库中这条数据是否存在，不存在则告诉用户不存在或者直接返回列表
        return render(request, "error.html", {"err_message": "该管理员已不存在！"})
        # return render(request, "admin_list.html")
    if request.method == "GET":  # 判断请求方式，如果是get那就直接返回编辑页面的信息即可
        form = AdminEditModelForms(instance=one_objects)
        return render(request, "change.html", {"form": form, "title": title})
    form = AdminEditModelForms(data=request.POST, instance=one_objects)  # 如果是修改后的，则看是否合法，合法则保存后返回列表
    if form.is_valid():
        form.save()
        return redirect("/admin/list/")
    return render(request, "change.html", {"form": form, "title": title})  # 如果不合法，那就返回我们的错误信息


def admin_delete(request, nid):
    Admin.objects.filter(id=nid).delete()
    return redirect("/admin/list/")


class AdminResetModelForms(BootStrapModelForm):
    confirm_password = forms.CharField(
        label="请再输入密码",
        widget=forms.PasswordInput
    )

    class Meta:
        model = Admin
        fields = ["password"]
        widgets = {
            "password": forms.PasswordInput(render_value=True)
        }

    def clean_password(self):
        password = self.cleaned_data.get("password")
        md5_password = md5(password)
        ex = Admin.objects.filter(id=self.instance.pk, password=md5_password).exists()
        if ex:
            raise ValidationError("不能与以前的密码相同")
        return md5_password

    def clean_confirm_password(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        md5_confirm_password = md5(confirm_password)
        if password != md5_confirm_password:
            raise ValidationError("密码不一致阿，请重新试一下")
        return confirm_password


def admin_reset(request, nid):
    """重置密码"""
    one_object = Admin.objects.filter(id=nid).first()
    title = "正在重置用户【{}】的密码".format(one_object.username)
    if request.method == "GET":
        form = AdminResetModelForms()
        return render(request, "change.html", {"form": form, "title": title})
    form = AdminResetModelForms(data=request.POST, instance=one_object)
    if form.is_valid():
        form.save()
        return redirect("/admin/list/")
    return render(request, "change.html", {"form": form, "title": title})
