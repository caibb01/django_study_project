import requests
from django.shortcuts import render, HttpResponse


def jarvisrenew(self=None):
    """ 贾维斯续签 """
    # 获取登陆的Token
    get_tokendata = {
        "url": "https://jarvis.myscrm.cn/m-application/login",
        "headers": {
            "content-type": "application/json;charset=UTF-8",
            "origin": "https://jarvis.myscrm.cn",
            "referer": "https://jarvis.myscrm.cn/m/application/applyboard/service?node_id=2"
        },
        "content": {
            "userName": "caibb01",
            "password": "@Cbb12345",
            "type": "account"
        }
    }
    result = requests.post(url=get_tokendata["url"], json=get_tokendata["content"],
                           headers=get_tokendata["headers"])
    token = result.json()["token"]
    # 请求贾维斯续签功能
    get_jsnewdata = {
        "url": "https://jarvis.myscrm.cn/m-operation/api/3337832029952811008/db_account/dbApplyRenew/5698/",
        "headers": {
            "content-type": "application/json;charset=UTF-8",
            "origin": "https://jarvis.myscrm.cn",
            "referer": "https://jarvis.myscrm.cn/m/application/applyboard/service?node_id=2",
            "Authorization": token
        },
    }
    result = requests.post(url=get_jsnewdata["url"],
                           headers=get_jsnewdata["headers"])
    # 断言续签结果
    if result.json()["status"].__contains__("Success"):
        # if "Success" in result.json()["status"]:
        return HttpResponse("续签成功")
    return HttpResponse("续签失败")
