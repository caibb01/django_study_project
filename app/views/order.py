from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import random
import json
from app.utils.bootstrap import BootStrapModelForm
from app.models import Order
from app.utils.pagination import Pagination


class OrderListModelForm(BootStrapModelForm):
    class Meta:
        model = Order
        fields = "__all__"
        exclude = ["Order_num", "admin"]


def order_list(request):
    if request.method == "GET":
        ordernum = request.GET.get("order_num", "")
        search_dict = {
            "Order_num__contains": ordernum
        }
        queryset = Order.objects.filter(**search_dict).order_by("-id")
        queryset_dict = Pagination(request, queryset=queryset)
        form = OrderListModelForm()
        content = {
            "form": form,
            "queryset": queryset_dict.page_queryset,
            "page_str_list": queryset_dict.html()
        }
        return render(request, "order_list.html", content)


@csrf_exempt
def ajax_add(request):
    form = OrderListModelForm(data=request.POST)
    print(form)
    if form.is_valid():
        form.instance.Order_num = datetime.now().strftime("%Y%m%d%H%M%S") + str(random.randint(1000, 9999))
        form.instance.admin_id = request.session.get("info")["id"]
        form.save()
        Responses = {
            "code": 200,
            "status": True
        }
        return HttpResponse(json.dumps(Responses))
    Responses = {"errors": form.errors}
    return HttpResponse(json.dumps(Responses, ensure_ascii=False))


from django.http.response import JsonResponse


def order_delete(request):
    """   删除订单   """
    uid = request.GET.get("uid")
    exists = Order.objects.filter(id=uid).exists()
    if not exists:
        return HttpResponse(json.dumps({"status": False, "error": "删除失败，所选择的数据已不存在"}))
    Order.objects.filter(id=uid).delete()
    return JsonResponse({"status": True, "success": "恭喜你，删除成功!"})


# JsonResponse({"status": True, "success": "恭喜你，删除成功!"})


def order_details(request):
    nid = request.GET.get("uid")
    one_object = Order.objects.filter(id=nid).values("Order_num", "title", "price").first()
    if not one_object:
        result = {
            "status": False,
            "error": "该数据不存在"
        }
    result = {
        "status": True,
        "data": one_object
    }
    return JsonResponse(result)

@csrf_exempt
def order_edit(request):
    input_uid = request.GET.get("uid")
    row_objecty = Order.objects.filter(id=input_uid).first()
    if not row_objecty:
        result = {
            "status": False,
            "tips": "数据不存在,请刷新重试一下"
        }
        return JsonResponse(result)
    form = OrderListModelForm(data=request.POST, instance=row_objecty)
    if form.is_valid():
        form.save()
        result = {
            "status": True,
            "code": 200
        }
        return JsonResponse(result)
    return JsonResponse({"status": False, "error": form.errors})
