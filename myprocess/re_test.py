import requests


class Cms(object):
    def __init__(self, name):
        self.name = name

    def login(self, user_zone):
        user_name = self.name
        print("我是{}，登录IP来自：{}".format(user_name, user_zone))
        # print()

class JarvisRenew():
    """ 贾维斯续签 """

    import requests

    def jsnew(self=None):
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
            return print("续签成功")
        return print("续签失败")


if __name__ == '__main__':
    # c = Cms("马老师")
    # c.login("广东")
    # Cms("马老师").login("广东")
    JarvisRenew.jsnew()
