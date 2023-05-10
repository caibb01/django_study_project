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


def chart_line(request):
    legend_list = ['需求', '缺陷', '任务', '数据问题', '新接口']
    xaxis_list = ['一月', '二月', '三月', '四月', '五月', '六月', '七月 ']
    series_list = [
        {
            "name": '需求',
            "type": 'line',
            "stack": 'Total',
            "data": [120, 132, 101, 134, 90, 230, 210]
        },
        {
            "name": '缺陷',
            "type": 'line',
            "stack": 'Total',
            "data": [220, 182, 191, 234, 290, 330, 310]
        },
        {
            "name": '任务',
            "type": 'line',
            "stack": 'Total',
            "data": [150, 232, 201, 154, 190, 330, 410]
        },
        {
            "name": '数据问题',
            "type": 'line',
            "stack": 'Total',
            "data": [320, 332, 301, 334, 390, 330, 320]
        },
        {
            "name": '新接口',
            "type": 'line',
            "stack": 'Total',
            "data": [820, 932, 901, 934, 1290, 1330, 1320]
        }
    ]
    result = {
        "status": True,
        "data": {
            "legend_list": legend_list,
            "xaxis_list": xaxis_list,
            "series_list": series_list,
        }
    }
    return JsonResponse(result)


def highcharts(request):

    return render(request,"highcharts.html")
