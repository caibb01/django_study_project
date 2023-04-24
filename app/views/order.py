from django.shortcuts import render, HttpResponse, redirect


def order_list(request):
    return render(request, "order_list.html")
