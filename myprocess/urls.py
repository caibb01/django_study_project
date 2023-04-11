"""myprocess URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app.views import depart, user, prettynum

urlpatterns = [

    # 部门管理
    path('depart/list/', depart.depart_list),
    path('depart/add/', depart.depart_add),
    path('depart/delete/', depart.depart_delete),
    path('depart/<int:edit_id>/edit/', depart.depart_edit),

    # 用户管理
    path('user/list/', user.user_list),
    path('user/add/', user.user_add),
    path('user/model/add/', user.user_model_list_add),
    path('user/<int:nid>/edit/', user.user_model_edit),
    path('user/<int:nid>/delete/', user.user_delete),

    # 靓号管理
    path('prettynum/list/', prettynum.prettynum_list),
    path('prettynum/add/', prettynum.prettynum_add),
    path('prettynum/<int:nid>/edit/', prettynum.prettynum_edit),
    path('prettynum/<int:nid>/delete/', prettynum.prettynum_delete),
]
