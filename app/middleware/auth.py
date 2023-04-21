from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse, render, redirect


class AuthMiddlware(MiddlewareMixin):
    def process_request(self,request):
        # 判断不需要鉴权就能访问的url
        if request.path_info == "/login/":
            return
        # 判断用户是否登陆过，登陆过就会存在一个session
        info_dict = request.session.get("info")
        print(info_dict)
        # session有值，那就通过这个中间件
        if info_dict:
            return
        # session没有值，无法通过这个中间件，下面这个是一个重定向操作
        # return redirect("/login/")
        return HttpResponse("您从未登陆过，请{}进入我们的系统吧！".format('<a href="/login">点击登陆</a>'))

# class M1MiddlewareMixin(MiddlewareMixin):
#     def process_request(self, request):
#         print("M1我来了")
#         return redirect('https://www.baidu.com/')
#
#     def process_response(self, request, response):
#         print("M1,走了 ")
#         return response
#
#
# class M2MiddlewareMixin(MiddlewareMixin):
#     def process_request(self, request):
#         print("M2我来了")
#
#     def process_response(self, request, response):
#         print("M2,走了 ")
#         return response
