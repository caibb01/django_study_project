from django.db import models


# Create your models here.

class Department(models.Model):
    """ 部门表 """
    title = models.CharField(verbose_name="标题", max_length=32)

    def __str__(self):
        return self.title


class UserInfo(models.Model):
    """ 员工表 """
    name = models.CharField(verbose_name="姓名", max_length=64)
    password = models.CharField(verbose_name="密码", max_length=64)
    account = models.DecimalField(verbose_name="账户余额", max_digits=10, decimal_places=2,
                                  default=0)  # m总个数，d是小数点后个数，m最大65，d最大30，默认账户余额为0
    age = models.IntegerField(verbose_name="年龄")
    create_time = models.DateTimeField(verbose_name="入职时间")

    """ 在html中引用时使用{{form.name}}，这里的name是哪个? """



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
    depart = models.ForeignKey(verbose_name="所属部门", to=Department, to_field="id", on_delete=models.CASCADE)  # 这里的depart不用加id，系统会自动添加的
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

# class role(models.Model):
#     name = models.CharField(max_length=64)
