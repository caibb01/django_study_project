from django.shortcuts import render, redirect, HttpResponse

from app.utils.pagination import Pagination
from app.models import Admin

def admin_list(request):
    """ 获取管理员 """
    search_detail = request.GET.get("num", '')
    # 将查询的条件字典化
    search_dict = {"username__contains": search_detail}

    """ 手机号的分页功能 """
    # 获取查询返回的page是第几页
    admin_queryset = Admin.objects.filter(**search_dict).order_by("id")

    page_object = Pagination(request, queryset=admin_queryset)

    context = {
        "search_detail":search_detail,
        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_str_list": page_object.html(),  # 页码
    }

    return render(request, 'admin_list.html', context)


