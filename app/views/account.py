from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, HttpResponse
from io import BytesIO

from app.utils.pagination import Pagination
from app.models import Admin
from django import forms
from app.utils.encrypt import md5
from app.utils.bootstrap import BootStrapModelForm, BootStrapForm
from app.utils.code_img import check_code

class LoginForm(BootStrapForm):
    username = forms.CharField(
        label="请输入用户名",
        widget=forms.TextInput,
        required=True

    )

    password = forms.CharField(
        label="请输入密码",
        widget=forms.PasswordInput(render_value=True),
        required=True
    )

    code = forms.CharField(
        label="请输入验证码",
        widget=forms.TextInput(),
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
    # 判断请求为查询，则直接返回列表信息即可
    if request.method == "GET":
        return render(request, "login.html", {"form": form})

    form = LoginForm(data=request.POST)

    # user_input_code = form.cleaned_data.pop("code")
    # print(user_input_code)
    # print(form.cleaned_data)



    if form.is_valid():
        # 验证成功，获取到的用户名和密码
        userinput_code = form.cleaned_data.pop("code")
        # 验证码的校验
        code = request.session.get("image_code", '')
        if userinput_code.upper() != code.upper():
            form.add_error("code","验证码错误")
            return render(request, "login.html", {"form": form})


        # 去数据库验证用户名和密码是否正确，获取用户对象、None
        admin_object = Admin.objects.filter(**form.cleaned_data).first()  # 判断用户在数据库是否存在
        # 验证用户是否存在，不存在则报错
        if not admin_object:
            form.add_error("password", "用户名或密码错误")
            return render(request, "login.html", {"form": form})

        # 用户名和密码与数据库匹配上的话
        # 网站生成随机字符串；写到用户浏览器的cookie中，在写入到session中
        request.session["info"] = {'id': admin_object.id, 'username': admin_object.username, }
        request.session.set_expiry(60*60*24*7)  # 设置登陆成功后的免登录时间，7天

        return redirect("/admin/list/")

    return render(request, "login.html", {"form": form})

def image_code(request):
    img,code_string = check_code() # 使用生成图片验证码的图片和code

    # 写入到自己的session中以便后续获取验证码再进行校验
    request.session['image_code'] = code_string
    # 給验证码的session设置60s超时，注意这里设置了，等一下整一个session都是60秒
    request.session.set_expiry(60)


    stream = BytesIO()  # 需要借用到一个内存动态展示到页面上
    img.save(stream,'png')
    return HttpResponse(stream.getvalue()) # 使用到页面上


def logout(request):
    request.session.clear()
    return redirect('/login/')
