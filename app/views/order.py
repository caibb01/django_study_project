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
    print(Responses)
    return HttpResponse(json.dumps(Responses, ensure_ascii=False))
