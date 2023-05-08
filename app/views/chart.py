from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse


def chart_list(request):
    """ 数据统计页面 """
    return render(request, "chart_list.html")


def chart_bar(request):
    """  构造柱状图的数据 """
    # 数据可以去数据库中获取
    legend = ["王志伟", "姚东秀", "杨陈"]
    x_Axis = ['衬衫', '羊毛衫', '雪纺衫', '裤子', '高跟鞋', '袜子']
    series_list = [
        {
            "name": "王志伟",
            "type": 'bar',
            "data": [5, 20, 36, 10, 10, 20]
        },
        {
            "name": "姚东秀",
            "type": 'bar',
            "data": [23, 54, 26, 34, 5, 10]
        },
        {
            "name": "杨陈",
            "type": 'bar',
            "data": [23, 54, 26, 34, 5, 10]
        },
    ]

    result = {
        "status": True,
        "data": {
            "series_list": series_list,
            "xAxis_list": x_Axis,
            "legend_list": legend
        }
    }
    print(result["data"]["series_list"])
    return JsonResponse(result)


def chart_Pie(request):
    # 从数据库获取数据
    db_series_list = [
        {"value": 1048, "name": '需求'},
        {"value": 735, "name": '缺陷'},
        {"value": 580, "name": '任务'},
        {"value": 484, "name": '数据问题'},
    ]
    result = {
        "status": True,
        "data_list": db_series_list
    }
    return JsonResponse(result)
