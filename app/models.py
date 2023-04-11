from django.db import models


# Create your models here.

class Department(models.Model):
    """ 部门表 """
    title = models.CharField(verbose_name="标题", max_length=32)

    def __str__(self):
        return self.title  # 输出对象时，定制显示的内容


class UserInfo(models.Model):
    """ 员工表 """
    name = models.CharField(verbose_name="姓名", max_length=64)
    password = models.CharField(verbose_name="密码", max_length=64)
    account = models.DecimalField(verbose_name="账户余额", max_digits=10, decimal_places=2,
                                  default=99999900)  # max_digits总个数，decimal_places是小数点后个数，
    # m最大65，d最大30，默认账户余额为0
    age = models.IntegerField(verbose_name="年龄")
    create_time = models.DateField(verbose_name="入职时间")  # DateTimeField 是存储年月日时分秒。不需要精确则DateField就可以了

    #  此时的员工表和部门表并没有关联关系，需要给一个关联关系
    #  1.用户表存储名称关联还是ID关联
    #       1.用户表名称
    #           1.大公司。查询的次数非常多，连表操作比较耗时。【加速查找，允许数据冗余】
    #       2.ID关联
    #           1.数据库范式（理论知识），常见开发都是这与。【节省存储开销】

    # 无约束
    # depart_id = models.ForeignKey( verbose_name="部门ID", max_length=64 )

    # 有约束
    # -to,与哪张表关联
    # -to_field,表中的那一列关联
    # 两种约束效果
    # 1.级联删除
    # 当部门删掉后，对应的用户也被删除
    depart = models.ForeignKey(verbose_name="所属部门", to=Department, to_field="id",
                               on_delete=models.CASCADE)  # 这里的depart不用加id，系统会自动添加的
    # 2.置空
    # 当部门删掉后，对应的用户depart_id的 id置空
    # depart_id = models.ForeignKey( verbose_name="", null=True,blank=True,to=Department,to_field="id",on_delete=models.SET_NULL,)

    # 在django中做的约束，以后gender只能写个1，或者2，就是能找到对应的变量
    gender_choices = (
        (1, "男"),
        (2, "女"),
    )
    # 注意Int的是整形还是Aut自增长类型
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices)  # 这么做的原因是节省存储。
    zone = models.CharField(verbose_name="地区", max_length=64)
    # 最后如果执行命令的时候一直提示这个表存在或者不存在的时候，请链接数据库直接创建一个表然后再执行删除的操作，再新增


class PrettyNum(models.Model):
    """ 靓号表 """
    mobile = models.CharField(verbose_name="手机号", max_length=64)  # 手机号要用到搜索,要正则,所以这里使用字符串
    price = models.IntegerField(verbose_name="价格")  # 这个是设置整数,若允许为空则 null=True,blank=True
    level_choices = (
        (1, "特级"),
        (2, "一级"),
        (3, "二级"),
        (4, "三级")
    )
    level = models.SmallIntegerField(verbose_name="等级", choices=level_choices, default=2)
    status_choices = (
        (1, "已售出"),
        (2, "已预订"),
        (3, "待销售"),
    )
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choices, default=3)
    zone = models.CharField(max_length=64, verbose_name="地区", null=True, blank=True)


class Admin(models.Model):
    """ 管理员 """
    username = models.CharField(verbose_name="用户名", max_length=64)
    password = models.CharField(verbose_name="密码", max_length=64)
