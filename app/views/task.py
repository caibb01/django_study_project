from django.shortcuts import render, redirect, HttpResponse
from django import forms
from django.core.exceptions import ValidationError
from app.utils.bootstrap import BootStrapModelForm
from django.views.decorators.csrf import csrf_exempt
from app.utils.pagination import Pagination
from app.models import Admin, Task
from app.utils.encrypt import md5

import json


class TaskAddModelForm(BootStrapModelForm):
    class Meta:
        model = Task
        fields = '__all__'
        widgets = {
            "detail": forms.TextInput()
        }


def task_list(request):
    form = TaskAddModelForm()
    return render(request, "task_list.html", {"form": form})


@csrf_exempt
def task_add(request):
    print(request.POST)
    form = TaskAddModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        data_dict = {"status": True}
        return HttpResponse(json.dumps(data_dict))

    data_dict = {"error": form.errors}
    return HttpResponse(json.dumps(data_dict, ensure_ascii=False))


# 加一个django的装饰器，因为Post时要获取csrf的token，加了下面这个就不会报403forbid
@csrf_exempt
def task_ajax(request):
    data_dict = {"status": True, 'data': [11, 22, 33, 44], "user": "李白", "age": 4}
    # return JsonResponse(data_dit)  # Django自带的字典转Json功能
    return HttpResponse(json.dumps(data_dict))
