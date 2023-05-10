from django import forms
from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from app.utils.bootstrap import BootStrapModelForm, BootStrap, BootStrapForm
from app.models import Boss, City
import os

"""  Form的上传写法  """


class UpForm(BootStrapForm):
    bootstrap_exclude_fields = ["img"]

    name = forms.CharField(label="姓名")
    age = forms.IntegerField(label="年龄")
    img = forms.FileField(label="头像")


def upload_form(request):
    title = "Form上传"
    form = UpForm()
    if request.method == 'GET':
        return render(request, "upload.html", {"form": form, "title": title})
    form = UpForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        # 读取到内容，写入到文件夹中并获取文件的路径
        image_object = form.cleaned_data.get("img")
        db_image_path = os.path.join("media", image_object.name)
        print(db_image_path)
        # 打开文件并且将文件保存至本地，将路径写入到数据库
        f = open(db_image_path, "wb")
        for chunk in image_object.chunks():
            f.write(chunk)
        f.close()
        Boss.objects.create(
            name=form.cleaned_data["name"],
            age=form.cleaned_data["age"],
            img=db_image_path
        )

        print(form.cleaned_data)
        return HttpResponse("上传成功了")
    return render(request, "upload.html", {"form": form, "title": title})


class UpModelForm(BootStrapModelForm):
    bootstrap_exclude_fields = ["img"]

    class Meta:
        model = City
        fields = '__all__'


def up_model_form(request):
    title = "ModelForm上传"
    form = UpModelForm()
    if request.method == "GET":
        return render(request, "upload.html", {"form": form, "title": title})
    form = UpModelForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        form.save()
        return
    return render(request, "upload.html", {"form": form, "title": title})


def city_list(request):
    queryst = City.objects.all()
    form = UpModelForm()
    return render(request, "city.html", {"form": form,"queryst":queryst })


def city_add(request):
    title = "新建城市的情况噢"
    form = UpModelForm()
    if request.method == "GET":
        return render(request, "upload.html", {"form": form, "title": title})
    form = UpModelForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        form.save()
        return redirect("/city/list")
    return render(request, "upload.html", {"form": form, "title": title})
