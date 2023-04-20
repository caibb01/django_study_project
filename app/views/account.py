from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, HttpResponse

from app.utils.pagination import Pagination
from app.models import Admin
from app.utils.encrypt import md5
from django import forms
from app.utils.bootstrap import BootStrapModelForm, BootStrapForm


class LoginForm(BootStrapForm):
    username = forms.CharField(
        label="用户名",
        widget=forms.TextInput,
        required=True

    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(render_value=True),
        required=True
    )

    def clean_password(self):
        password = self.cleaned_data.get("password")
        return md5(password)


# class LoginModelForm(forms.ModelForm):
#     class Meta:
#         model = Admin
#         fields = ['username','password']
def login(request):
    form = LoginForm
    if request.method == "GET":
        return render(request, "login.html", {"form": form})

    form = LoginForm(data=request.POST)
    if form.is_valid():
        admin_object = Admin.objects.filter(**form.cleaned_data).first()  # 判断用户在数据库是否存在
        # 验证用户是否存在，不存在则报错
        if not admin_object:
            form.add_error("password", "用户名或密码错误")
            return render(request, "login.html", {"form": form})

        # 用户名和密码与数据库匹配上的话
        # 网站生成随机字符串；写到用户浏览器的cookie中，在写入到session中
        request.session["info"] = {'id': admin_object.id, 'username': admin_object.username}
        return redirect("/admin/list/")
    return render(request, "login.html", {"form": form})


def logout(request):
    request.session.clear()
    return redirect('/login/')
