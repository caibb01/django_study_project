class Cms(object):
    def __init__(self, name):
        self.name = name

    def login(self, user_zone):
        user_name = self.name
        print("我是{}，登录IP来自：{}".format(user_name, user_zone))
        # print()


if __name__ == '__main__':
    # c = Cms("马老师")
    # c.login("广东")
    Cms("马老师").login("广东")
